


import frappe
from frappe import _
from dynamic.api import get_allowed_stoc_use_submit
DOMAINS = frappe.get_active_domains()


def before_save_stock_entry(doc, *args, **kwargs):
    if "WEH" in DOMAINS:
        get_allowed_stoc_use_submit(doc,doc.get("from_warehouse"))





DOMAINS = frappe.get_active_domains()
def update_target_warehouse(doc, *args, **kwargs):
	if "WEH" in DOMAINS:
		for row in doc.items:
			row.warehouse = doc.set_warehouse
		frappe.db.commit()