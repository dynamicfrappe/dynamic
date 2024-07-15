import frappe
from frappe import _
from frappe.model.document import Document
DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def validate(doc, method):
    if "Qaswaa" in DOMAINS:
        if not doc.sales_team:
            frappe.throw("Sales Team cannot be empty for domain 'Qaswaa'")

        

        

        