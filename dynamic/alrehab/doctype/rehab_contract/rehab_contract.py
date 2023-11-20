# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RehabContract(Document):
	def validate(self):
		...

	def before_submit(self):
		if self.maintenance_deposit_installments_items:
			for row in self.maintenance_deposit_installments_items:
				self.initiate_installment_entry(row)


	@frappe.whitelist()
	def initiate_installment_entry(self,row):
		installment_entry = frappe.new_doc("installment Entry")
		installment_entry.item = row.item
		installment_entry.type = self.installment_entry_type
		installment_entry.installment_value = row.installment_value
		installment_entry.total_value = row.installment_value
		installment_entry.outstanding_value = row.installment_value
		installment_entry.due_date = row.due_date
		installment_entry.status = "Under collection"
		installment_entry.customer = self.unit
		installment_entry.insert()
