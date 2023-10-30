# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 


from frappe.model.document import Document

class Journalinstallment(Document):
	def validate(self) :
		if self.journal_type == "Contract" and self.contracted== 0:
			#create contract 
			contract = frappe.new_doc("Rehab Contract") 
			contract.unit = self.unit
			contract.installment_entry_type = self.type 
			contract.save()
			self.contracted = 1
			self.contract = contract.name