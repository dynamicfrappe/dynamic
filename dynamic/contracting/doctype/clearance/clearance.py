# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

from shutil import ignore_patterns
from erpnext.accounts.doctype.account.account import get_account_currency
from erpnext.accounts.party import get_party_account
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_invoice
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder, make_sales_invoice
from frappe.utils import (
	DATE_FORMAT,
	add_days,
	add_to_date,
	cint,
	comma_and,
	date_diff,
	flt,
	getdate,
    nowdate,
get_link_to_form
)

class Clearance(Document):
	def on_submit(self):
		self.update_comparison()
		self.update_purchase_order()
		self.create_deduction_je()
	def on_cancel(self):
		self.update_purchase_order(cancel=1)
	def update_comparison(self):
		if self.comparison and self.items and self.clearance_type == "Outcoming":
			doc = frappe.get_doc("Comparison",self.comparison)
			for clearence_item in self.items:
				for comparison_item in doc.item:
					if clearence_item.clearance_item == comparison_item.clearance_item:
						## set previous qty and completed qty in clearence
						clearence_item.previous_qty       = comparison_item.completed_qty
						clearence_item.completed_qty      = clearence_item.current_qty + clearence_item.previous_qty
						clearence_item.completed_percent  = (float(clearence_item.completed_qty) / float(clearence_item.qty)) *100 if clearence_item.qty else 0
						clearence_item.previous_percent   = (float(clearence_item.previous_qty) / float(clearence_item.qty)) *100 if clearence_item.qty else 0
						clearence_item.previous_amount	  = float(clearence_item.previous_qty) * float(clearence_item.price)

						### update comparison
						comparison_item.completed_qty    += clearence_item.current_qty
						comparison_item.completed_percent = ( comparison_item.completed_qty / clearence_item.qty) *100 if clearence_item.qty else 0
						comparison_item.remaining_qty	  = clearence_item.qty - comparison_item.completed_qty
						comparison_item.remaining_percent = (comparison_item.remaining_qty / comparison_item.qty) * 100
						comparison_item.remaining_amount  = float(comparison_item.remaining_qty) * float(clearence_item.price)

						### update remaining in clearence
						clearence_item.remaining_qty = clearence_item.qty - comparison_item.completed_qty
						clearence_item.remaining_percent = (comparison_item.remaining_qty / comparison_item.qty) * 100
						clearence_item.remaining_amount = float(comparison_item.remaining_qty) * float(clearence_item.price)

			self.save()
			doc.save()
		else:
			pass
	@frappe.whitelist()
	def create_payment_entry(self):
		if not self.customer:
			return "Please Set Customer"
		company         = frappe.db.get_value("Global Defaults", None, "default_company")
		company_doc     = frappe.get_doc("Company", company)
		cash_account    = company_doc.default_cash_account
		project_account = company_doc.capital_work_in_progress_account
		recivable_account= company_doc.default_receivable_account
		precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

		journal_entry = frappe.new_doc('Journal Entry')
		journal_entry.company = company
		journal_entry.posting_date = nowdate()
		# credit
		credit_row = journal_entry.append("accounts", {})
		credit_row.party_type = "Customer"
		credit_row.account     = recivable_account
		credit_row.party	   = self.customer
		credit_row.credit_in_account_currency	   = flt(self.grand_total, precision)
		credit_row.reference_type = self.doctype
		credit_row.reference_name = self.name
		# debit
		debit_row = journal_entry.append("accounts", {})
		debit_row.account	   = project_account
		debit_row.debit_in_account_currency		   = flt(self.grand_total, precision)
		debit_row.reference_type = self.doctype
		debit_row.reference_name = self.name
		journal_entry.save()
		journal_entry.submit()
		form_link = get_link_to_form(journal_entry.doctype,journal_entry.name)
		frappe.msgprint("Journal Entry %s Create Successfully"%form_link)

		# second journal
		s_journal_entry = frappe.new_doc('Journal Entry')
		s_journal_entry.company = company
		s_journal_entry.posting_date = nowdate()
		# credit
		s_credit_row = s_journal_entry.append("accounts", {})
		s_credit_row.account = cash_account
		s_credit_row.credit_in_account_currency = flt(self.grand_total, precision)
		s_credit_row.reference_type = self.doctype
		s_credit_row.reference_name = self.name
		# debit
		s_debit_row = s_journal_entry.append("accounts", {})
		s_debit_row.account    = recivable_account
		s_debit_row.party_type = "Customer"
		s_debit_row.party = self.customer
		s_debit_row.debit_in_account_currency = flt(self.grand_total, precision)
		s_debit_row.reference_type = self.doctype
		s_debit_row.reference_name = self.name
		s_journal_entry.save()
		form_link = get_link_to_form(journal_entry.doctype, journal_entry.name)
		frappe.msgprint("Journal Entry %s Create Successfully" %form_link)
		# self.paid=1
		# self.save()
		frappe.db.sql("""update tabClearance set paid=1 where name='%s'"""%self.name)
		frappe.db.commit()

	@frappe.whitelist()
	def can_create_invoice(self,doctype):
		invoice = frappe.db.get_value(doctype , {"clearance":self.name , "docstatus":["<" , 2]},'name')
		return 0 if invoice else 1

	def create_deduction_je(self):
		if getattr(self,'deductions') and self.total_deductions:
			if self.clearance_type == "incoming" :
				if not self.purchase_order :
					frappe.throw(_("Please set Purchase Order"))
				if not self.supplier :
					frappe.throw(_("Please set Supplier"))
				self.create_deduction_supplier_je()
			if self.clearance_type == "Outcoming" :
				if not self.sales_order :
					frappe.throw(_("Please set Sales Order"))
				if not self.customer :
					frappe.throw(_("Please set Customer"))
				self.create_deduction_customer_je()

	
	
	def create_deduction_supplier_je(self):
		je = frappe.new_doc("Journal Entry")
		je.posting_date = nowdate()
		je.voucher_type = 'Journal Entry'
		je.company = self.company
		je.remark = f'Deduction against  Supplier {self.supplier} Deduction: ' + self.doctype +" " + self.name
		supplier_account = get_party_account("Supplier", self.supplier, self.company)
		if not supplier_account :
			frappe.throw(_("Please Account for supplier {}").format(self.supplier))
		
		je.append("accounts", {
		"account": supplier_account  ,
		"account_currency": get_account_currency(supplier_account),
		"debit_in_account_currency": flt(self.total_deductions or 0),
		"party_type":"Supplier",
		"party":self.supplier,
		"reference_type" : self.doctype,
		"reference_name" : self.name
		})
		for row in self.deductions :
			je.append("accounts", {
			"account": row.account  ,
			"account_currency": get_account_currency(row.account),
			"credit_in_account_currency": row.amount,
			"cost_center": row.cost_center,
			"project": self.project,
			"reference_type" : self.doctype,
			"reference_name" : self.name
			})
		je.submit()


	def create_deduction_customer_je(self):
		je = frappe.new_doc("Journal Entry")
		je.posting_date = nowdate()
		je.voucher_type = 'Journal Entry'
		je.company = self.company
		je.remark = f'Deduction against  Customer {self.customer} Deduction: ' + self.doctype +" " + self.name
		customer_account = get_party_account("Customer", self.customer, self.company)
		if not customer_account :
			frappe.throw(_("Please Account for Customer {}").format(self.customer))
		
		je.append("accounts", {
		"account": customer_account  ,
		"account_currency": get_account_currency(customer_account),
		"credit_in_account_currency": flt(self.total_deductions or 0),
		"party_type":"Customer",
		"party":self.customer,
		"project": self.project,
		"reference_type" : self.doctype,
		"reference_name" : self.name
		})
		for row in self.deductions :
			je.append("accounts", {
			"account": row.account  ,
			"account_currency": get_account_currency(row.account),
			"debit_in_account_currency": row.amount,
			"project": self.project,
			"reference_type" : self.doctype,
			"reference_name" : self.name
			})
		je.submit()







	def update_purchase_order(self,cancel = False):
		if self.purchase_order and self.items and self.clearance_type == "incoming":
			for item in self.items :
				try : 
					purchase_order_item = frappe.get_doc("Purchase Order Item",item.purchase_order_item)
					if cancel :
						purchase_order_item.completed_qty -= item.current_qty
					else :
						purchase_order_item.completed_qty += item.current_qty

					purchase_order_item.completed_percent  = (float(purchase_order_item.completed_qty) / float(purchase_order_item.qty)) *100
					purchase_order_item.completed_amount  = (float(purchase_order_item.rate) * float(purchase_order_item.completed_qty))

					if cancel :
						purchase_order_item.remaining_qty = max(purchase_order_item.qty,purchase_order_item.qty - purchase_order_item.completed_qty)
					else:
						purchase_order_item.remaining_qty = min(0,purchase_order_item.qty - purchase_order_item.completed_qty)

					purchase_order_item.remaining_percent  = (float(purchase_order_item.remaining_qty) / float(purchase_order_item.qty)) *100
					purchase_order_item.remaining_amount  = (float(purchase_order_item.rate) * float(purchase_order_item.remaining_qty))
					purchase_order_item.save()
				except :
					pass

				
@frappe.whitelist()
def clearance_make_purchase_invoice (source_name , target_doc=None) :
	doc = frappe.get_doc("Clearance",source_name)
	invoice = make_purchase_invoice(doc.purchase_order)
	invoice.set_missing_values()
	invoice.is_contracting = 1
	invoice.clearance = doc.name
	invoice.comparison = doc.comparison
	# invoice.set("items",[])
	for row in doc.items :
		invoice_item = [x for x in invoice.items if x.po_detail == row.purchase_order_item]
		if len(invoice_item) > 0 :
			invoice_item = invoice_item [0]
			invoice_item.qty = row.current_qty
		


	try :
		invoice.save(ignore_permissions=1)
	except Exception as e:
		frappe.throw(str(e))	
	# invoice.submit()	
	# doc.purchase_invoice = pi.name
	# doc.save()
	return invoice
				
@frappe.whitelist()
def clearance_make_sales_invoice (source_name , target_doc=None) :
	doc = frappe.get_doc("Clearance",source_name)
	invoice = make_sales_invoice(doc.sales_order)
	invoice.set_missing_values()
	invoice.is_contracting = 1
	invoice.clearance = doc.name
	invoice.comparison = doc.comparison
	for row in doc.items :
		invoice_item = [x for x in invoice.items if x.item_code == row.clearance_item]
		if len(invoice_item) > 0 :
			invoice_item = invoice_item [0]
			invoice_item.qty = row.current_qty
	try :
		invoice.save(ignore_permissions=1)
	except Exception as e:
		frappe.throw(str(e))
	# doc.purchase_invoice = pi.name
	# doc.save()
	return invoice



# def make_purchase_invoice(source_name, target_doc=None):
# @frappe.whitelist()
# def make_purchase_invoice(source_name, target_doc=None):
# 	return get_mapped_purchase_invoice(source_name, target_doc)


















