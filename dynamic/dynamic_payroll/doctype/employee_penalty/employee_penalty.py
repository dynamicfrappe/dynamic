# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
class EmployeePenalty(Document):
	
	@frappe.whitelist()
	def set_total_amount(self):
		pass




@frappe.whitelist()
def create_addtional_salary(doc):
	penalty_doc = json.loads(doc)
	addtionall_salary_doc = frappe.new_doc('Additional Salary')
	addtionall_salary_doc.employee = penalty_doc.employee
	addtionall_salary_doc.salary_component = penalty_doc.salary_component #
	addtionall_salary_doc.payroll_date = penalty_doc.payroll_effect_date 
	addtionall_salary_doc.amount = penalty_doc.amount 
	addtionall_salary_doc.save()




