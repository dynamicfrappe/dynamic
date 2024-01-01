# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
from frappe import _


class Conservationorder(Document):
	@frappe.whitelist()
	def get_warranties(self , serial_number):
		item = frappe.db.get_value('Serial No', serial_number ,["item_code", "warranty_expiry_date"], as_dict=1)

		item_code = frappe.get_value(
               "Item", item.get("item_code"), ["item_name", "description"], as_dict=1)
		return item.get("item_code") ,item_code.get("item_name") , item_code.get("description") ,item.get("warranty_expiry_date")

	def before_validate(self):
		self.calculate_total_cost()

	def before_submit(self):
		self.create_conservation()

	def calculate_total_cost(self):
		sum = 0
		for item in self.items :
			if item.rate:
				sum += item.rate
		for item in self.service_items:
			if item.rate:
				sum += item.rate
		if self.transfer_cost :
			sum += self.transfer_cost
		self.total_cost = sum

	def create_conservation(self):
		conservation = frappe.new_doc("Conservation")
		conservation.customer = self.customer
		conservation.customer_name = self.customer_name
		conservation.customer_primary_contact = self.customer_primary_contact
		conservation.customer_primary_address = self.customer_primary_address
		conservation.support = self.support
		conservation.location = self.location
		conservation.type_for_request = self.type_for_request
		conservation.name_of_maintenance = self.name_of_maintenance
		conservation.number = self.number
		conservation.warranties = self.warranties
		conservation.machines = self.machines
		conservation.customer_comment = self.customer_comment
		conservation.description_of_maintenance_manager = self.description_of_maintenance_manager
		conservation.maintenance_type = self.maintenance_type
		conservation.type_of_maintenance = self.type_of_maintenance
		conservation.items = self.items
		conservation.service_items = self.service_items
		conservation.transfer_cost = self.transfer_cost
		conservation.total_cost = self.total_cost
		conservation.engineering_name = self.engineering_name
		conservation.insert()

		lnk = get_link_to_form(conservation.doctype, conservation.name)
		frappe.msgprint(_("{} {} was Created").format(
		conservation.doctype, lnk))