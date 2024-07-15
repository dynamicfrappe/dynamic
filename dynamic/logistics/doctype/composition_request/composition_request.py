# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
from frappe import _

DOMAINS = frappe.get_active_domains()

class CompositionRequest(Document):
	@frappe.whitelist()
	def fetch_survey_template(self , survey):
		survey_doc = frappe.get_doc("Survey" , survey)
		for row in survey_doc.survey_template:
			self.append("survey_template" , row)
			
	@frappe.whitelist()
	def get_items(self):
		sales_order = frappe.get_doc("Sales Order" , self.sales_order)
		return sales_order.items
	
	@frappe.whitelist()
	def set_address_and_numbers(self):
		sql = f'''
			SELECT 
			 	CP.phone , C.address 
			FROM 
			  	`tabContact Phone` CP
			INNER JOIN 
				`tabContact` C
			ON 
				C.name = CP.parent
			INNER JOIN 
				`tabDynamic Link` DL
			ON 
				C.name = DL.parent
			WHERE 
				link_name = '{self.customer}'
			limit 3
			'''
		data = frappe.db.sql(sql , as_dict = 1)
		self.address = ''
		self.phone_number_1 = ''
		self.phone_number_2 = ''
		self.phone_number_3 = ''

		if data :
			if len(data) == 1:
				self.address = data[0]['address']
				self.phone_number_1 = data[0]['phone']
			if len(data) == 2:
				self.address = data[0]['address']
				self.phone_number_1 = data[0]['phone']
				self.phone_number_2 = data[1]["phone"]
			if len(data) == 3:
				self.address = data[0]['address']
				self.phone_number_1 = data[0]['phone']
				self.phone_number_2 = data[1]["phone"]
				self.phone_number_3 = data[2]["phone"]
		
				

	def on_submit(self):
		if 'Logistics' in DOMAINS :
			self.create_composition_order()

	def create_composition_order(self):
		composition_order = frappe.new_doc("Composition Order")
		composition_order.date = self.date 
		composition_order.sales_order = self.sales_order
		composition_order.status = self.status
		composition_order.customer = self.customer
		composition_order.password = self.password
		composition_order.attachment = self.attachment
		composition_order.items = self.items
		composition_order.address = self.address
		composition_order.phone_number_1 = self.phone_number_1
		composition_order.phone_number_2 = self.phone_number_2
		composition_order.phone_number_3 = self.phone_number_3
		composition_order.link_location = self.link_location
		composition_order.customer_comment = self.customer_comment
		composition_order.location_is_ready = self.location_is_ready
		composition_order.insert()
		self.db_set("composition_order",composition_order.name)

		lnk = get_link_to_form(composition_order.doctype, composition_order.name)
		frappe.msgprint(_("{} {} was Created").format(
		composition_order.doctype, lnk))


