# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.data import  get_link_to_form 
from frappe.model.document import Document


Domains=frappe.get_active_domains()
class installmentEntry(Document):
	def on_change(self) :
		if "Rehab"  in Domains :
			self.create_journal_entry()

	def create_journal_entry(self):
		if not self.is_clamed :
			journal_entry = frappe.new_doc("Journal Entry")
			journal_entry.posting_date = self.due_date
			company = frappe.defaults.get_user_default("Company")
			debitor_account = frappe.get_value("Company" , company , "default_receivable_account")
			journal_entry.installment_entry = self.name
			journal_entry.append("accounts" ,
						{"account" :debitor_account , "party_type" : "Customer",
		                 "party":self.customer , "debit_in_account_currency" :self.total_value ,
						 "credit_in_account_currency" : 0.00})
			journal_entry.append("accounts" ,
						{"account" :self.income_account ,
						 "debit_in_account_currency" : 0.00,
						 "credit_in_account_currency" : self.total_value})
			journal_entry.insert()
			journal_entry.submit()

			lnk = get_link_to_form(journal_entry.doctype, journal_entry.name)
			frappe.msgprint(_("{} {} was Created").format(
				journal_entry.doctype, lnk))
