# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
DOMAINS = frappe.get_active_domains()


class CompositionOrder(Document):
	@frappe.whitelist()
	def get_items(self):
		sales_order = frappe.get_doc("Sales Order" , self.sales_order)
		return sales_order.items
	
	@frappe.whitelist()
	def update_status(self):
		frappe.db.sql(f""" 
				UPDATE 
					`tabComposition Request` CO
				SET 
					CO.status = '{self.status}' 
				WHERE 
					CO.composition_order = '{self.name}' 
					AND
					CO.docstatus = 1
				""")
		
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
			self.create_composition()

	def create_composition(self):
		composition = frappe.new_doc("Composition")
		composition.date = self.date 
		composition.sales_order = self.sales_order
		composition.status = self.status
		composition.customer = self.customer
		composition.items = self.items
		composition.address = self.address
		composition.phone_number_1 = self.phone_number_1
		composition.phone_number_2 = self.phone_number_2
		composition.phone_number_3 = self.phone_number_3
		composition.link_location = self.link_location
		composition.engineers = self.engineers
		composition.customer_comment = self.customer_comment
		composition.location_is_ready = self.location_is_ready
		composition.insert()
		composition.save()
		self.composition = composition.name
		self.submit()

		lnk = get_link_to_form(composition.doctype, composition.name)
		frappe.msgprint(_("{} {} was Created").format(
		composition.doctype, lnk))
