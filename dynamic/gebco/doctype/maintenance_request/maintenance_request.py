# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceRequest(Document):
	def validate(self):
		pass
		
			
			#self.save()
	def after_insert(self):
		if self.employee and self.status == "Pending":
			self.assign_request_to_employee()
			self.status = "Assined"
	def assign_request_to_employee(self):
		doc = frappe.new_doc("ToDo")
		doc.owner = self.employee
		doc.description = self.description
		doc.reference_type = "Maintenance Request"
		doc.reference_name = self.name
		doc.save()


@frappe.whitelist()
def create_maintenance_request(source_name, target_doc=None):
	doc = frappe.get_doc("Maintenance Request",source_name)
	maint_temp = frappe.new_doc("Maintenance Template")
	maint_temp.maintenance_contract = doc.maintenance_contract
	maint_temp.problem = doc.description
	maint_temp.customer = doc.company_name
	maint_temp.car_numbers = doc.car_numbers
	if maint_temp.maintenance_contract:
		contract = frappe.get_doc("Maintenance Contract",maint_temp.maintenance_contract)
		maint_temp.warehouse = contract.warehouse
		maint_temp.include_spare_part = contract.include_spare_parts

	return maint_temp
	

