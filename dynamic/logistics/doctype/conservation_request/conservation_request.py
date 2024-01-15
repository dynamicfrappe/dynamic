# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form , now

class ConservationRequest(Document):
	def before_naming(self):
		self.user = frappe.session.user
	
	def before_submit(self):
		self.validate_warranties()

	def on_submit(self):
		self.create_Conservation_order()

	@frappe.whitelist()
	def get_warranties(self , serial_number):
		item = frappe.db.get_value('Serial No', serial_number ,["item_code", "warranty_expiry_date"], as_dict=1)

		item_code = frappe.get_value(
               "Item", item.get("item_code"), ["item_name", "description"], as_dict=1)
		return item.get("item_code") ,item_code.get("item_name") , item_code.get("description") ,item.get("warranty_expiry_date")

	@frappe.whitelist()
	def get_maintenance_item(self):
		conservation_requestes = frappe.get_all("Conservation Request" ,
										filters = {"docstatus" : 1} , pluck = "name") 

		if  not self.get("maintenance") :
			for req in conservation_requestes :
				self.append("maintenance" , {"conservation_request" : req})


	def create_Conservation_order(self):
		conservation_order = frappe.new_doc("Conservation order")
		conservation_order.customer = self.customer
		conservation_order.customer_name = self.customer_name
		conservation_order.customer_primary_contact = self.customer_primary_contact
		conservation_order.customer_primary_address = self.customer_primary_address
		conservation_order.support = self.support
		conservation_order.location = self.location
		conservation_order.type_for_request = self.type_for_request
		conservation_order.name_of_maintenance = self.name_of_maintenance
		conservation_order.number = self.number
		conservation_order.warranties = self.warranties
		conservation_order.machines = self.machines
		conservation_order.customer_comment = self.customer_comment
		conservation_order.insert()

		lnk = get_link_to_form(conservation_order.doctype, conservation_order.name)
		frappe.msgprint(_("{} {} was Created").format(
		conservation_order.doctype, lnk))
	
	def validate_warranties(self):
		for warranty in self.warranties :
			if warranty.idx == 1 :
				if not warranty.warranty :
					self.type_for_request = "Maintenance"
				if warranty.warranty < now() :
					self.type_for_request = "Out of Warranty"
				if warranty.warranties >= now() :
					self.type_for_request = "Out of Warranty"