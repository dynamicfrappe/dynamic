# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

from erpnext.accounts.doctype.account.account import get_account_currency
import frappe
from frappe import _
from erpnext.setup.utils import get_exchange_rate
from frappe.model.document import Document
import erpnext
from frappe.utils.data import flt
from frappe.utils import get_link_to_form
class PayandReceiptDocument(Document):
	@frappe.whitelist()
	def get_conversion_rate (self):
		company_currency = erpnext.get_company_currency(self.company)
		self.exchange_rate = get_exchange_rate(self.currency, company_currency, self.posting_date)

	def before_insert (self):
		self.journal_entry = ''
	# def validate (self):
	# 	self.journal_entry = ''
		# company_currency = erpnext.get_company_currency(self.company)
		# account_currency = get_account_currency(self.account)
		# if account_currency not in [company_currency , self.currency] :

	def on_submit(self)	:
		self.create_journal_entry()
	
	def on_cancell(self):
		self.cancel_journal_entry()

	def create_journal_entry (self):
		company_currency = erpnext.get_company_currency(self.company)
		je = frappe.new_doc("Journal Entry")
		je.posting_date = self.posting_date
		je.voucher_type = 'Journal Entry'
		je.company = self.company
		je.cheque_no = self.reference_no
		je.cheque_date = self.reference_date
		je.remark = f'Payment against {self.document_type} Document: ' + self.name + '\n' + (self.notes or "")


		debit_account = self.account if self.document_type == "Receive" else self.against_account
		debit_account_currency = get_account_currency(debit_account)
		# debit_account_currency = self.currency

		debit_cost_center = self.cost_center if self.document_type == "Receive" else ''
		debit_project = self.project if self.document_type == "Receive" else ''

		credit_account = self.account if self.document_type == "Pay" else self.against_account
		credit_account_currency = get_account_currency(credit_account)
		# credit_account_currency = self.currency




		# handle debit account currency



		debit_in_account_currency = flt(self.amount)
		debit_exchange_rate = flt(self.exchange_rate)

		if debit_account_currency != self.currency :
			if debit_account_currency == company_currency :
					debit_exchange_rate = 1
					debit_in_account_currency = flt(self.base_amount)

			else :
				debit_exchange_rate = get_exchange_rate(debit_account_currency, company_currency, self.posting_date)
				debit_in_account_currency = flt(self.amount) * flt(debit_exchange_rate)


		# handle debit account currency
		credit_in_account_currency = flt(self.amount)
		credit_exchange_rate = flt(self.exchange_rate)
		if credit_account_currency != self.currency :
			if credit_account_currency == company_currency :
					credit_exchange_rate = 1
					credit_in_account_currency =  flt(self.base_amount)

			else :
				credit_exchange_rate = get_exchange_rate(credit_account_currency, company_currency, self.posting_date)
				credit_in_account_currency = flt(self.base_amount) * flt(credit_exchange_rate)







		je.multi_currency = 1 if credit_account_currency != debit_account_currency else 0


		je.append("accounts", {
		"account": debit_account  ,
		"account_currency": debit_account_currency,
		"exchange_rate": flt(debit_exchange_rate),
		"debit_in_account_currency": flt(debit_in_account_currency),
		"debit_in_company_currency": flt(self.base_amount),
		"reference_type" : self.doctype,
		"reference_name" : self.name
		})

		je.append("accounts", {
		"account": credit_account  ,
		"account_currency": credit_account_currency,
		"exchange_rate": flt(credit_exchange_rate),
		"credit_in_account_currency": flt(credit_in_account_currency),
		"credit_in_company_currency": flt(self.base_amount),
		"cost_center": self.cost_center,
		"project": self.project,
		"user_remark" : self.notes or "",
		"reference_type" : self.doctype,
		"reference_name" : self.name
		})
		# for i in je.accounts :
		# 	frappe.msgprint(f"account : {i.account} | account_currency : {i.account_currency} | debit_in_account_currency : {i.debit_in_account_currency} | credit_in_account_currency : {i.credit_in_account_currency}")
		je.submit()
		self.journal_entry = je.name
		lnk = get_link_to_form(je.doctype,je.name)
		frappe.msgprint(_("Journal Entry {} was created").format(lnk))

	def cancel_journal_entry (self):
		if getattr(self,'journal_entry') :
			je = frappe.get_doc("Journal Entry",self.journal_entry)
			if (je.docstatus == 1) :
					je.cancel()
			self.journal_entry = ''