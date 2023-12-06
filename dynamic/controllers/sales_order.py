



import frappe
from frappe import _
from dynamic.qaswaa.controllers.sales_order_api import validate_item_qty_reserved

Domains=frappe.get_active_domains()

def validate_sales_order(self , event):
    if "Qaswaa" in Domains :
        validate_item_qty_reserved(self,event)
    
 



