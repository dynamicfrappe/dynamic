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

def set_total_gross_weight(self, *args, **kwargs):
    if "Megaback" in DOMAINS:
        for item in self.items:
            item_doctype = frappe.get_doc("Item", item.item_code)
            item.gross_weight =  item_doctype.gross_weight
            if item.qty and item.gross_weight:
                item.total_gross_weight = float(item.qty) * float(item.gross_weight)