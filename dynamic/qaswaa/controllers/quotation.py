import frappe
from frappe import _
DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def validate(self, method):
    if "Qaswaa" in DOMAINS:
        item_discount_rates(self)
    if "Healthy Corner" in DOMAINS:
        item_discount_rate(self)


@frappe.whitelist()       
def item_discount_rate(self):
    item_discount_rate = self.discount_item or 0
    for item in self.items:
        item.discount_percentage = item_discount_rate
        if item_discount_rate is not None:
            item.discount_amount = item.price_list_rate * (item_discount_rate / 100)
        else:
            item.discount_amount = 0  
        item.rate = item.price_list_rate - item.discount_amount
        item.amount = item.rate * item.qty
    
@frappe.whitelist()       
def item_discount_rates(self):
    item_discount_rate = self.item_discount_rate or 0
    for item in self.items:
        item.discount_percentage = item_discount_rate
        if item_discount_rate is not None:
            item.discount_amount = item.price_list_rate * (item_discount_rate / 100)
        else:
            item.discount_amount = 0  
        item.rate = item.price_list_rate - item.discount_amount
        item.amount = item.rate * item.qty  
        






