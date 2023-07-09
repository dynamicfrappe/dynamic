


import frappe
from frappe import _



@frappe.whitelist()
def create_first_contract(source_name):
    item_doc = frappe.get_doc("Item",source_name)
    new_quotation = frappe.new_doc("Quotation")
    new_quotation.append('items',{
        'item_code':item_doc.name,
        'item_name':item_doc.item_name,
        'uom':item_doc.stock_uom,
        'qty':1,
    })
    return new_quotation
    