import frappe

from frappe.utils import add_days, nowdate, today
from dynamic.terra.doctype.payment_entry.payment_entry import get_party_details

@frappe.whitelist()
def get_iem_sub_uom(item_code,uom,qty):
    item  = frappe.get_doc("Item",item_code)
    # if len(item.uoms) >=1:
    #     if item.uoms[1].uom == uom:
    #         return {
    #         "sub_uom":item.uoms[1].uom,
    #         "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
    #         "qty_as_per_sub_uom": qty
    #     }
    #     return {
    #         "sub_uom":item.uoms[1].uom,
    #         "sub_uom_conversation_factor":item.uoms[1].conversion_factor,
    #         "qty_as_per_sub_uom": float(qty or 0) / float(item.uoms[1].conversion_factor or 0)
    #     }
    # return {
    #         "sub_uom":"",
    #         "sub_uom_conversation_factor":0,
    #         "qty_as_per_sub_uom": 0
    #     }
    for u in item.uoms:
        if u.is_sub_uom:
            if u.uom !=uom:
                return {
                    "sub_uom":u.uom,
                    "sub_uom_conversation_factor":u.conversion_factor,
                    "qty_as_per_sub_uom": float(qty or 0) / float(u.conversion_factor or 0)
                }

            if u.uom == uom :
                return {
                    "sub_uom":u.uom,
                    "sub_uom_conversation_factor":u.conversion_factor,
                    "qty_as_per_sub_uom": qty
                }

    return {
            "sub_uom":"",
            "sub_uom_conversation_factor":0,
            "qty_as_per_sub_uom": 0
        }



# material request type ------------> purchase
# validate if no item   ------------> validation error 
@frappe.whitelist()
def create_sales_order_from_opportunity(source_name, target_doc=None):
    source_doc = frappe.get_doc("Opportunity",source_name)
    doc = frappe.new_doc("Sales Order")
    if source_doc.opportunity_from == "Customer":
        doc.customer = source_doc.party_name
    if len(source_doc.items)> 0:
        for item in source_doc.items:
            item_doc = frappe.get_doc("Item",item.item_code)
            doc.append("items",{
                "item_code"     : item.item_code,
                "qty"           : item.qty,
                "item_name"     : item.item_name,
                "description"   : item.item_name,
                "uom"           : item_doc.stock_uom,
                "stock_uom"     : item_doc.stock_uom
            })

    return doc

@frappe.whitelist()
def create_material_request_from_opportunity(source_name, target_doc=None):
    source_doc = frappe.get_doc("Opportunity",source_name)
    doc = frappe.new_doc("Material Request")
    doc.purpose = "Purchase"
    if len(source_doc.items)> 0:
        for item in source_doc.items:
            item_doc = frappe.get_doc("Item",item.item_code)
            doc.append("items",{
                "item_code"     : item.item_code,
                "qty"           : item.qty,
                "item_name"     : item.item_name,
                "description"   : item.item_name,
                "uom"           : item_doc.stock_uom,
                "stock_uom"     : item_doc.stock_uom,
                "schedule_date" : today()
            })
    return doc




@frappe.whitelist()
def get_quotation_item(quotation,*args,**Kwargs):
    doc = frappe.get_doc("Quotation",quotation)
    return doc.items
    
@frappe.whitelist()
def get_payment_entry_quotation(source_name):
    qutation_doc = frappe.get_doc('Quotation',source_name)
    pe = frappe.new_doc("Payment Entry")
    pe.payment_type = "Receive"
    pe.mode_of_payment = "Cash"
    pe.party_type = qutation_doc.quotation_to
    pe.party = qutation_doc.party_name
    pe.party_name = qutation_doc.customer_name
    cash_detail = get_all_apyment_for_quotation(source_name)
    pe.paid_amount = cash_detail.get("outstand") #modify to outstand amount
    row = pe.append('references',{})
    row.reference_doctype = "Quotation"
    row.reference_name = source_name
    row.total_amount = qutation_doc.grand_total
    row.outstanding_amount = cash_detail.get("outstand") #modify to outstand amount
    cst_account = get_party_details(company=qutation_doc.company,date=None,
    party_type=qutation_doc.quotation_to, 
    party=qutation_doc.party_name,
    cost_center=None)
    pe.part_balance = cst_account.get('party_balance')
    pe.paid_from = cst_account.get('party_account')
    pe.paid_from_account_currency = cst_account.get('party_account_currency')
    pe.paid_from_account_balance = cst_account.get('account_balance')
    return pe



def get_all_apyment_for_quotation(qutation_name):
    sql=f'''
            select tper.parent,tper.reference_name ,tper.total_amount, 
            IFNULL(SUM(tper.allocated_amount),0) total_paid,
            (tper.total_amount-IFNULL(SUM(tper.allocated_amount),0))outstand
            from `tabPayment Entry Reference` tper
            where tper.reference_name='{qutation_name}' 
            GROUP by tper.reference_name
    '''
    data = frappe.db.sql(sql,as_dict=1)
    return data[0]
    
