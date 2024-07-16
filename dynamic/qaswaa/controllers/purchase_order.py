import frappe
from frappe import _
DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def validate(doc, method):
    if "Qaswaa" in DOMAINS:
        item_discount_rate = doc.item_discount_rate
        for item in doc.items:
            item.discount_percentage = item_discount_rate
            item.discount_amount = item.price_list_rate * (item_discount_rate / 100)
            item.rate = item.price_list_rate - item.discount_amount
            item.amount = item.rate * item.qty