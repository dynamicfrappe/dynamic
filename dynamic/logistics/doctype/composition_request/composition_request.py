# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CompositionRequest(Document):
	@frappe.whitelist()
	def get_items(self , sales_order):
		sales_order = frappe.get_doc("Sales Order" , sales_order)
		self.items = []
		for item in sales_order.items :
			self.append("items" , item)
