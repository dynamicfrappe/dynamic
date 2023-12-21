# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
DOMAINS = frappe.get_active_domains()

class POContainer(Document):
	@frappe.whitelist()
	def get_purchase_order_details(self ,purchase_order):
		if purchase_order :
			purchase_order = frappe.get_value(
               "Purchase Order", purchase_order, ["supplier", "grand_total"], as_dict=1)
			return purchase_order.get("supplier") , purchase_order.get("grand_total")
		
	@frappe.whitelist()
	def change_status(self):
		self.db_set("status", "Delivered")
		
	def before_submit(self):
		if 'Logistics' in DOMAINS: 
			for purchase_order_container in self.purchase_order_containers:
				frappe.db.set_value('Purchase Order',purchase_order_container.purchase_order,'has_shipped','1')
