# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Maintenancedeposit(Document):
	def on_submit(self) :
		#create installment entry 
		for i in self.maintenance_deposit_installments_items :
			if not i.paid : 
				entry = frappe.new_doc("installment Entry") 
				entry.reference_doc = "Maintenance deposit"
				entry.document = self.name 
				entry.customer = self.unit
				entry.installment_value = i.installment_value
				entry.due_date = i.due_date
				entry.save()
				# i.reference_entry = entry.name
				frappe.db.set_value("Maintenance Deposit installments Items" , i.name , 'reference_entry' , entry.name )
				frappe.db.commit()

   #remove linked docs from installment Entry /  Claiming Entry
	def remove_linked_docs_entry(self ,entry) :
		"""
		cancel all ref journal entry  
		"""
		for doc in entry.claiming_entry :
			if doc.type == "Journal Entry" :
				journal_entry = frappe.get_doc("Journal Entry" ,doc.document )
				journal_entry.cancel()
				# journal_entry.save(ignore_permissions = True)
			pass
		#pass
   #remove linked docs from installment Entry /  Paid Entry
	def remove_payments_links_docs(self ,entry) :
		"""
		cancel all ref payment entry  
		"""
		for doc in entry.paid_entry :
			if doc.type == "Payment Entry" :
				payment_entry = frappe.get_doc("Payment Entry" ,doc.document )
				payment_entry.cancel()
	def on_cancel(self) :
		entries = frappe.get_list("installment Entry" , {"reference_doc" :"Maintenance deposit" , 
						   "document" :self.name })
		for entry in entries :
			doc = get_installment_entry(entry)
			self.remove_linked_docs_entry(doc)
			self.remove_payments_links_docs(doc)
			doc.status = "Canceled"
			doc.save()
		

# us this remove_linked_docs_entry / remove_payments_links_docs
def get_installment_entry( entry) :
	doc = frappe.get_doc("installment Entry" , entry)
	return doc