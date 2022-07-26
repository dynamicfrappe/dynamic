from erpnext import get_default_company
import frappe
from frappe import _

def check_return_account(doc):
    if doc.is_return:
        company = frappe.get_doc("Company",get_default_company())
        if company.get("sales_return_account"):
            default_sales_account = company.get("default_income_account")
            for item in doc.items:
                if item.get("default_income_account") != company.get("sales_return_account"):
                    frappe.msgprint("Default Income Account Changed in Line %s"%item.idx)


def validate_sales_invoices(doc):

    # validate sales invocie linked with sales order 
    for line in doc.items :
        if not line.sales_order : 
            frappe.throw(_(f"""You can not add Sales Invocie withou Sales Order 
                                Please Check item {line.item_name}"""))

        #check reservation 
    if doc.update_stock ==1  : 
        #close Item Reservation 
        frappe.throw("validate")