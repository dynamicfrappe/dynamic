# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from dynamic.contracting.doctype.sales_order.sales_order import set_delivery_date
from erpnext import get_default_company
from erpnext.selling.doctype.sales_order.sales_order import is_product_bundle
from frappe.model.mapper import get_mapped_doc
import json
from frappe import _

from frappe.utils.data import flt, get_link_to_form, nowdate
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from six import string_types
class Tender(Document):
	@frappe.whitelist()
	def get_payment_account(self):
		self.payment_account = ""
		if self.mode_of_payment :
			self.payment_account = get_bank_cash_account(self.mode_of_payment, self.company).get("account")

	@frappe.whitelist()
	def create_terms_journal_entries(self):
		company = frappe.get_doc("Company" , self.company)
		projects_account = company.capital_work_in_progress_account
		if not projects_account :
			frappe.throw("Please set Capital Work in Progress Account in Company Settings")
		

		je = frappe.new_doc("Journal Entry")
		je.posting_date = nowdate()
		je.voucher_type = 'Journal Entry'
		je.company = company.name
		je.cheque_no = self.reference_no
		je.cheque_date = self.reference_date
		je.remark = f'Journal Entry against {self.doctype} : {self.name}'


		je.append("accounts", {
		"account": projects_account  ,
		"credit_in_account_currency": flt(self.terms_sheet_amount),
		"reference_type" : self.doctype,
		"reference_name" : self.name,
		"cost_center": self.terms_sheet_cost_center,
		"project": self.project,
		})


		je.append("accounts", {
		"account":   self.project_account  ,
		"debit_in_account_currency": flt(self.terms_sheet_amount),
		"reference_type" : self.doctype,
		"reference_name" : self.name
		})
		
		# for i in je.accounts :
		# 	frappe.msgprint(f"account : {i.account} | account_currency : {i.account_currency} | debit_in_account_currency : {i.debit_in_account_currency} | credit_in_account_currency : {i.credit_in_account_currency}")
		je.submit()



		lnk = get_link_to_form(je.doctype,je.name)
		frappe.msgprint(_("Journal Entry {} was created").format(lnk))
		
	@frappe.whitelist()
	def create_terms_payment(self):
		company = frappe.get_doc("Company" , self.company)
		projects_account = company.capital_work_in_progress_account
		if not projects_account :
			frappe.throw("Please set Capital Work in Progress Account in Company Settings")
		

		


		payment_je = frappe.new_doc("Journal Entry")
		payment_je.posting_date = nowdate()
		payment_je.voucher_type = 'Journal Entry'
		payment_je.company = company.name
		payment_je.cheque_no = self.reference_no
		payment_je.cheque_date = self.reference_date
		payment_je.remark = f'Payment against {self.doctype} : {self.name}'


		payment_je.append("accounts", {
		"account": self.payment_account  ,
		"credit_in_account_currency": flt(self.terms_sheet_amount),
		"reference_type" : self.doctype,
		"reference_name" : self.name,
		"cost_center": self.terms_sheet_cost_center,
		"project": self.project,
		})

		payment_je.append("accounts", {
		"account": projects_account  ,
		"debit_in_account_currency": flt(self.terms_sheet_amount),
		"reference_type" : self.doctype,
		"reference_name" : self.name
		})

		payment_je.submit()
		payment_lnk = get_link_to_form(payment_je.doctype,payment_je.name)
		self.terms_paid=1
		self.save()
		frappe.msgprint(_("Journal Entry {} was created").format(payment_lnk))
	
	def on_submit(self):
		self.validate_status()
		if self.terms_paid and self.terms_sheet_amount > 0 and self.current_status == "Approved" :
			self.create_terms_journal_entries()
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
