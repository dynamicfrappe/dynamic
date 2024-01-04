


import frappe
from frappe import _
from dynamic.api import get_allowed_stoc_use_submit
DOMAINS = frappe.get_active_domains()


def before_save_stock_entry(doc, *args, **kwargs):
    if "WEH" in DOMAINS:
        get_allowed_stoc_use_submit(doc, doc,doc.get("from_warehouse"))


