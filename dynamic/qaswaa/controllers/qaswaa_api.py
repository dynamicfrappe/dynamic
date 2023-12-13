

import frappe
from frappe.utils import add_days, cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate


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
