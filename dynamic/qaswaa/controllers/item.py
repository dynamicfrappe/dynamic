import frappe 
from frappe import _
import requests
import json


DOMAINS = frappe.get_active_domains()

def after_insert(self , method):
    if "Item Integration" in DOMAINS:
        stock_settings = frappe.get_doc("Stock Settings")
        if stock_settings.enable_item_itegration == 1:
            url = stock_settings.url_item_integration
            token = stock_settings.token_item_integration
            
            payload = json.dumps({
                "doctype": "Item",
                "name":self.name,
                "item_name": self.item_name,
                "item_group": self.item_group,
                "stock_uom": self.stock_uom,
                "is_stock_item": self.is_stock_item,
                "include_item_in_manufacturing": self.include_item_in_manufacturing
                })
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                frappe.msgprint("Item Created")




