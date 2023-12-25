

import frappe
from frappe.utils import add_days, cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate

from erpnext.selling.doctype.quotation.quotation import _make_customer
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def create_purchase_invoice(doc_name):
    so_doc = frappe.get_doc('Sales Order',doc_name)
    pi = frappe.new_doc("Purchase Invoice")
    for row in so_doc.items:
        if flt(row.required_qty) > 0:
            pi.append('items',{
                "item_code":row.item_code,
                "item_name":row.item_name,
                "warehouse":row.warehouse,
                "qty":row.required_qty,
            })
    
    return pi





@frappe.whitelist()
def create_qaswaa_sales_order(source_name: str, target_doc=None):
	if not frappe.db.get_singles_value(
		"Selling Settings", "allow_sales_order_creation_for_expired_quotation"
	):
		quotation = frappe.db.get_value(
			"Quotation", source_name, ["transaction_date", "valid_till"], as_dict=1
		)
		if quotation.valid_till and (
			quotation.valid_till < quotation.transaction_date or quotation.valid_till < getdate(nowdate())
		):
			frappe.throw(_("Validity period of this quotation has ended."))

	return _make_sales_order(source_name, target_doc)


def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	customer = _make_customer(source_name, ignore_permissions)
	ordered_items = frappe._dict(
		frappe.db.get_all(
			"Sales Order Item",
			{"prevdoc_docname": source_name, "docstatus": 1},
			["item_code", "sum(qty)"],
			group_by="item_code",
			as_list=1,
		)
	)

	def set_missing_values(source, target):
		if customer:
			target.customer = customer.name
			target.customer_name = customer.customer_name
		if source.referral_sales_partner:
			target.sales_partner = source.referral_sales_partner
			target.commission_rate = frappe.get_value(
				"Sales Partner", source.referral_sales_partner, "commission_rate"
			)
		target.flags.ignore_permissions = ignore_permissions
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(obj, target, source_parent):
		balance_qty = obj.qty - ordered_items.get(obj.item_code, 0.0)
		target.qty = balance_qty if balance_qty > 0 else 0
		target.stock_qty = flt(target.qty) * flt(obj.conversion_factor)

		if obj.against_blanket_order:
			target.against_blanket_order = obj.against_blanket_order
			target.blanket_order = obj.blanket_order
			target.blanket_order_rate = obj.blanket_order_rate

	doclist = get_mapped_doc(
		"Quotation",
		source_name,
		{
			"Quotation": {
				"doctype": "Sales Order",
				"validation": {"docstatus": ["=", 1]}},
			"Quotation Item": {
				"doctype": "Sales Order Item",
				"field_map": {"parent": "prevdoc_docname"},
				"postprocess": update_item,
				"condition": lambda doc: doc.qty > 0,
			},
			"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
			"Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
			"Payment Schedule": {"doctype": "Payment Schedule", "add_if_empty": True},
		},
		target_doc,
		set_missing_values,
		ignore_permissions=ignore_permissions,
	)

	# postprocess: fetch shipping address, set missing values
	# doclist.set_onload("", True)

	return doclist