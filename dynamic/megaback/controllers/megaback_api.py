import frappe
from frappe import _

DOMAINS = frappe.get_active_domains()

def set_volumes(self, *args, **kwargs):
    if "Megaback" in DOMAINS:
        total = 0.0
        for item in self.items:
            item_doctype = frappe.get_doc("Item", item.item_code)
            item.volume =  item_doctype.volume
            
            if item.qty and item.volume:
                item.total_volume = float(item.qty) * float(item.volume)
                total += float(item.total_volume) or 0

        self.items_total_volume = total
