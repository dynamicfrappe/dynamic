from erpnext.selling.doctype.sales_order.sales_order import is_product_bundle
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import flt, now_datetime, nowdate

@frappe.whitelist()
def update_comparison (self,fun=''):
    if 'Contracting' not in frappe.get_active_domains():
        return
    for item in self.items :
        if getattr(item,"comparison" , None) and getattr(item,"comparison_item" , None):
            try :
                comparison_item = frappe.get_doc("Comparison Item",item.comparison_item)
                if fun == "on_submit":
                    comparison_item.purchased_qty = (comparison_item.purchased_qty or 0 ) + item.qty
                    comparison_item.remaining_purchased_qty = max(0,(comparison_item.qty or 0 ) - comparison_item.purchased_qty)
                elif fun == "on_cancel":
                    comparison_item.purchased_qty = min(0,(comparison_item.purchased_qty or 0 ) - item.qty)
                    comparison_item.remaining_purchased_qty = max(comparison_item.qty,(comparison_item.qty or 0 ) - comparison_item.purchased_qty)  
                comparison_item.save()
            except:
                pass




@frappe.whitelist()
def make_clearence_doc(source_name, target_doc=None, ignore_permissions=False):
    def postprocess(source, target):
        set_missing_values(source, target)

    def set_missing_values(source, target):
        target.flags.ignore_permissions = True
        target.update({'purchase_order_date': source.schedule_date})
        target.update({'clearance_type': "incoming"})
        target.update({'clearance_date': nowdate()})
        target.update({'purchase_taxes_and_charges_template':source.taxes_and_charges})
        target.update({'total_after_tax':source.grand_total or source.rounded_total})
        target.update({'comparison':source.comparison })
        target.update({'down_payment_insurance_rate_':source.down_payment_insurance_rate })
        target.update({'payment_of_insurance_copy_of_operation_and_initial_delivery':source.payment_of_insurance_copy })
        target.update({'purchase_order':source.name })


    def update_item(source, target, source_parent):
        target.qty =  source.qty - source.completed_qty
        target.current_qty  = target.qty
        target.total_price =  target.qty * source.rate
        target.purchase_order = source_parent.name
        target.purchase_order_item = source.name



    doclist = get_mapped_doc("Purchase Order", source_name, {
        "Purchase Order": {
            "doctype": "Clearance",

        },
        "Purchase Order Item": {
            "doctype": "Clearance Items",
            "field_map": {
                "item_code":"clearance_item",
                "rate":"price",
                # "qty":"qty",
                # "qty":"current_qty",
                # "amount":"total_price",
                "uom":"uom"
            },
            "add_if_empty": True,
            "postprocess":update_item,
			"condition": lambda doc: doc.completed_qty < doc.qty  and not is_product_bundle(doc.item_code)
        },
        "Purchase Taxes and Charges": {
            "doctype": "Purchase Taxes and Charges Clearances",
            "field_map": {
                "charge_type": "charge_type",
                # "account_head": "account_head",
                # "description":"description"
            },
            "add_if_empty": True
        },
    }, target_doc,postprocess, ignore_permissions=ignore_permissions)

    return doclist
