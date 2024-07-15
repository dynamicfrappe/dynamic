# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form , now

class ConservationRequest(Document):
	def before_naming(self):
		self.user = frappe.session.user
	
	def before_validate(self):
		self.validate_warranties()

	def on_submit(self):
		self.create_Conservation_order()

	@frappe.whitelist()
	def fetch_survey_template(self , survey):
		survey_doc = frappe.get_doc("Survey" , survey)
		for row in survey_doc.survey_template:
			self.append("survey_template" , row)
			
	@frappe.whitelist()
	def get_warranties(self , serial_number):
		item = frappe.db.get_value('Serial No', serial_number ,["item_code", "warranty_expiry_date"], as_dict=1)

		item_code = frappe.get_value(
               "Item", item.get("item_code"), ["item_name", "description" , "stock_uom"], as_dict=1)
		res = {
				'item_code':item_code.get("item_code"),
				'item_name':item_code.get("item_name"),
				'description':item_code.get("description"),
				'warranty_expiry_date':item.get("warranty_expiry_date"),
				'item_code':item.get("item_code"),
				'uom': item_code.get("stock_uom")
			}
		return res

	def create_Conservation_order(self):
		conservation_order = frappe.new_doc("Conservation order")
		conservation_order.customer = self.customer
		conservation_order.customer_name = self.customer_name
		conservation_order.customer_primary_contact = self.customer_primary_contact
		conservation_order.customer_primary_address = self.customer_primary_address
		conservation_order.support = self.support
		conservation_order.support_reason = self.support_reason
		conservation_order.not_support = self.not_support
		conservation_order.not_support_reason = self.not_support_reason
		conservation_order.location = self.location
		conservation_order.type_for_request = self.type_for_request
		conservation_order.name_of_maintenance = self.name_of_maintenance
		conservation_order.number = self.number
		conservation_order.warranties = self.warranties
		conservation_order.machines = self.machines
		conservation_order.customer_comment = self.customer_comment
		conservation_order.insert()
		self.reference = conservation_order.name

		lnk = get_link_to_form(conservation_order.doctype, conservation_order.name)
		frappe.msgprint(_("{} {} was Created").format(
		conservation_order.doctype, lnk))
	
	def validate_warranties(self):
		if not self.warranties :
			self.type_for_request = "Maintenance"