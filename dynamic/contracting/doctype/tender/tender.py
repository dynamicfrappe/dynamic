# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Tender(Document):
	def on_submit(self):
		self.validate_status()
	def validate_status(self):
		if self.current_status == "Pending":
			frappe.throw("Cannot Submit Please Approve Or Reject")
		elif self.current_status == "Approved" and self.comparison:
			try:
				doc = frappe.get_doc("Comparison",self.comparison)
				if doc.insurance_value_rate != self.insurance_rate:
					doc.insurance_value_rate = self.insurance_rate
					doc.insurance_value = self.insurance_amount
					doc.save()
			except:
				print("error")
				pass
