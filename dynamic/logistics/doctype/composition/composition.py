# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Composition(Document):
	def before_submit(self):
		self.complete_status()

	@frappe.whitelist()
	def get_items(self):
		sales_order = frappe.get_doc("Sales Order" , self.sales_order)
		return sales_order.items
	
	@frappe.whitelist()
	def update_status(self):
		frappe.db.sql(f""" 
				UPDATE 
					`tabComposition Order` CO
				SET 
					CO.status = '{self.status}' 
				WHERE 
					CO.composition = '{self.name}' 
					AND
					CO.docstatus = 1
				""")
	
	@frappe.whitelist()
	def fetch_survey_template(self , survey):
		survey_doc = frappe.get_doc("Survey" , survey)
		for row in survey_doc.survey_template:
			self.append("survey_template" , row)

	def complete_status(self):
		self.status="Completed"
		composition_order = frappe.get_last_doc("Composition Order" , {"composition" : self.name})
		composition_request = frappe.get_last_doc("Composition Request" , {"composition_order" : composition_order.name})
		composition_order.db_set("status","Completed")
		composition_request.db_set("status","Completed")

		