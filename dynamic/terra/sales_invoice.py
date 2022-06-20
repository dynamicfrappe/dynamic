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