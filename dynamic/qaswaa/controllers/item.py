import frappe 
from frappe import _
import requests
import json


DOMAINS = frappe.get_active_domains()



@frappe.whitelist()
def after_insert(self):
    if "Item Integration" in DOMAINS: 
        stock_settings = frappe.get_single("Stock Settings") 
        if stock_settings.enable_item_itegration:
            url = stock_settings.url_item_integration
            token = stock_settings.token_item_integration
            self = json.loads(self)
            if not url or not token:
                frappe.throw("Item integration URL or Token is not configured in Stock Settings.")
            
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
            }

            params = {
                "fields": json.dumps(["name"]),
                "filters": json.dumps([["Item", "item_name", "=", self.get("item_name")]])  
                }
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    if json.loads(response.text).get("data"):
                        frappe.msgprint(_("This Item name already exists"))
                        return 

            except requests.exceptions.RequestException as e:
                frappe.log_error(f"Item integration failed: {str(e)}", "Item Integration Error")
                frappe.msgprint("Failed to create item in Integration System. Check error logs.")

            
            


            payload = json.dumps({
                "doctype": "Item",
                "item_name": self.get("item_name"),
                "item_group": self.get("item_group"),
                "stock_uom": self.get("stock_uom"),
                "is_stock_item": self.get("is_stock_item"),
                "include_item_in_manufacturing": self.get("include_item_in_manufacturing")
            })
            
            try:
                response = requests.post(url, headers=headers, data=payload)
                if response.status_code == 200:
                    frappe.msgprint("Item Created")
                else:
                    frappe.msgprint(_("Item Group didn't exists"))
            except requests.exceptions.RequestException as e:
                frappe.log_error(f"Item integration failed: {str(e)}", "Item Integration Error")
                frappe.msgprint(_("Failed to create item in Integration System. Check error logs."))


