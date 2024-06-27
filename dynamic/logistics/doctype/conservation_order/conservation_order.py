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

	def validate_enginners(self):
		if self.engineering_name :
			for engineer in self.engineering_name :
				if engineer.from1 >= engineer.to :
					frappe.throw(_(f"From must be before to of row {engineer.idx} in enginnering table"))
				else :
					sql = f'''
						select 
							* 
						from 
							`tabEngineering Name` e
						where
							e.parenttype = "Conservation order"
								and 
							e.employee = '{engineer.employee}' 
								and
							('{engineer.from1}' between e.from1 and e.to 
								or 
							'{engineer.to}' between e.from1 and e.to )
						'''
					if engineer.name  :
						sql = sql +f"and e.name  != '{engineer.name}'"
					data = frappe.db.sql(sql, as_dict = 1)
					if data :
						frappe.throw(_(f"This range of row assigned to this employee in {data[0]['from1']} - {data[0]['to']} "))
	
	def before_validate(self):
		self.validate_enginners()

	def before_submit(self):
		self.calculate_total_cost()

	def on_submit(self):
		self.create_conservation()

	def calculate_total_cost(self):
		sum = 0
		if self.items:
			for item in self.items :
				if item.rate:
					sum += item.rate
		if self.service_items:
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
		if self.type_of_maintenance :
			conservation.type_of_maintenance = self.type_of_maintenance
		if self.items :
			conservation.items = self.items
		if self.service_items :
			conservation.service_items = self.service_items
		if self.transfer_cost :
			conservation.transfer_cost = self.transfer_cost
		if self.total_cost :
			conservation.total_cost = self.total_cost
		conservation.engineering_name = self.engineering_name
		conservation.insert()

		lnk = get_link_to_form(conservation.doctype, conservation.name)
		frappe.msgprint(_("{} {} was Created").format(
		conservation.doctype, lnk))