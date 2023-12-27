# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
from frappe import _

DOMAINS = frappe.get_active_domains()

class CompositionRequest(Document):
	@frappe.whitelist()
	def get_items(self):
		sales_order = frappe.get_doc("Sales Order" , self.sales_order)
		return sales_order.items

	def on_submit(self):
		if 'Logistics' in DOMAINS :
			self.create_composition_order()

	def create_composition_order(self):
		composition_order = frappe.new_doc("Composition Order")
		composition_order.date = self.date 
		composition_order.sales_order = self.sales_order
		composition_order.status = self.status
		composition_order.customer = self.customer
		composition_order.items = self.items
		composition_order.address = self.address
		composition_order.phone_number_1 = self.phone_number_1
		composition_order.phone_number_2 = self.phone_number_2
		composition_order.phone_number_3 = self.phone_number_3
		composition_order.link_location = self.link_location
		composition_order.customer_comment = self.customer_comment
		composition_order.location_is_ready = self.location_is_ready
		composition_order.insert()
		composition_order.submit()
		self.db_set("composition_order",composition_order.name )

		lnk = get_link_to_form(composition_order.doctype, composition_order.name)
		frappe.msgprint(_("{} {} was Created").format(
		composition_order.doctype, lnk))


