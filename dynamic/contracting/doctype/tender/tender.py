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
			print("from el if")
			try:
				doc = frappe.get_doc("Comparison",self.comparison)
				t = (doc.insurance_value) +  (doc.delivery_insurance_value)
				if doc.insurance_value_rate != self.insurance_rate:
					print("from if ttttttttttttt",t)
					doc.insurance_value_rate = self.insurance_rate
					doc.insurance_value = self.insurance_amount
					doc.docstatus = 1
					doc.total_insurance = (doc.insurance_value) +  (doc.delivery_insurance_value)
					doc.tender = self.name
					doc.tender_status = self.current_status
					self.total_insurance = (doc.insurance_value) +  (doc.delivery_insurance_value)
					doc.save(ignore_permissions=True)
				# doc.submit(ignore_permissions=True)
			except:
				print("error")
				pass
