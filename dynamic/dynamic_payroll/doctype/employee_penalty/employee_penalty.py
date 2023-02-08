# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeePenalty(Document):
	
	@frappe.whitelist()
	def set_total_amount(self):
		pass








