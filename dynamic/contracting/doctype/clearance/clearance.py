# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

from re import template
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
from frappe.utils.data import now_datetime


class Clearance(Document):
	def on_submit(self):
		self.update_comparison_tender()
		self.update_purchase_order()
		self.create_deduction_je()

	def on_cancel(self):
		self.update_purchase_order(cancel=1)

	# def update_comparison(self):
	#     if self.comparison and self.items and self.clearance_type == "Outcoming":
	#         doc = frappe.get_doc("Comparison", self.comparison)
	#         for clearence_item in self.items:
	#             for comparison_item in doc.item:
	#                 if clearence_item.clearance_item == comparison_item.clearance_item:
	#                     # set previous qty and completed qty in clearence
	#                     clearence_item.previous_qty = comparison_item.completed_qty
	#                     clearence_item.completed_qty = clearence_item.current_qty + \
	#                         clearence_item.previous_qty
	#                     clearence_item.completed_percent = (float(
	#                         clearence_item.completed_qty) / float(clearence_item.qty)) * 100 if clearence_item.qty else 0
	#                     clearence_item.previous_percent = (float(
	#                         clearence_item.previous_qty) / float(clearence_item.qty)) * 100 if clearence_item.qty else 0
	#                     clearence_item.previous_amount = float(
	#                         clearence_item.previous_qty) * float(clearence_item.price)

	#                     # update comparison
	#                     comparison_item.completed_qty += clearence_item.current_qty
	#                     comparison_item.completed_percent = (
	#                         comparison_item.completed_qty / clearence_item.qty) * 100 if clearence_item.qty else 0
	#                     comparison_item.remaining_qty = clearence_item.qty - comparison_item.completed_qty
	#                     comparison_item.remaining_percent = (
	#                         comparison_item.remaining_qty / comparison_item.qty) * 100
	#                     comparison_item.remaining_amount = float(
	#                         comparison_item.remaining_qty) * float(clearence_item.price)

	#                     # update remaining in clearence
	#                     clearence_item.remaining_qty = clearence_item.qty - comparison_item.completed_qty
	#                     clearence_item.remaining_percent = (
	#                         comparison_item.remaining_qty / comparison_item.qty) * 100
	#                     clearence_item.remaining_amount = float(
	#                         comparison_item.remaining_qty) * float(clearence_item.price)

	#         self.save()
	#         doc.save()
	#     else:
	#         pass


	def update_comparison_tender(self):
		if self.comparison and self.items and self.clearance_type == "Outcoming":
			doc = frappe.get_doc("Comparison", self.comparison)
			tender_doc = None
			if doc.tender :
				tender_doc = frappe.get_doc("Tender",doc.tender)
			for clearence_item in self.items:
				for comparison_item in doc.item:
					if clearence_item.clearance_item == comparison_item.clearance_item:
						result = get_item_price(self.comparison,clearence_item.clearance_item,clearence_item.clearance_state,clearence_item.current_qty) or {}
						state_percent = result.get("state_percent") or 100
						completed_percent = state_percent  * (clearence_item.current_qty or 0) /( comparison_item.qty or 1)
						completed_amount = clearence_item.total_price

						comparison_item.previous_percent = completed_percent
						comparison_item.previous_amount = completed_amount

						comparison_item.completed_percent = (comparison_item.completed_percent or 0) + completed_percent 
						comparison_item.completed_amount = (comparison_item.completed_amount or 0) + completed_amount



						comparison_item.remaining_percent = 100- completed_percent 
						comparison_item.remaining_amount = (comparison_item.total_price or 0) - completed_amount



						log = frappe.new_doc("Comparison Item Log")
						log.posting_date = now_datetime()
						log.state = clearence_item.clearance_state
						log.state_percent = clearence_item.state_percent
						log.item_code = clearence_item.clearance_item
						log.item_name = clearence_item.clearance_item_name
						log.description = clearence_item.clearance_item_description
						log.uom = clearence_item.uom
						log.qty = clearence_item.current_qty or 0
						log.price = clearence_item.current_price or 0
						log.comparison = doc.name
						log.reference_type = self.doctype
						log.reference_name = self.name
						log.submit()
					# if tender_doc :
						# for tamplate_item in tender_doc.states_template or [] :
							# if tamplate_item.state == clearence_item.clearance_state:
						# 		tamplate_item.current =  (completed_percent / tamplate_item.percent)*100
						# 		# frappe.msgprint(str(tamplate_item.current))
						# 		tamplate_item.completed = (tamplate_item.completed or 0) + tamplate_item.current
						# 		tamplate_item.remaining = 100 - tamplate_item.completed
								

					
					
						
			self.save()
			doc.save()
			if tender_doc :
				tender_doc.save()
		else:
			pass

	@frappe.whitelist()
	def create_payment_entry(self):
		if not self.customer:
			return "Please Set Customer"
		company = frappe.db.get_value(
			"Global Defaults", None, "default_company")
		company_doc = frappe.get_doc("Company", company)
		cash_account = company_doc.default_cash_account
		project_account = company_doc.capital_work_in_progress_account
		recivable_account = company_doc.default_receivable_account
		precision = frappe.get_precision(
			"Journal Entry Account", "debit_in_account_currency")

		journal_entry = frappe.new_doc('Journal Entry')
		journal_entry.company = company
		journal_entry.posting_date = nowdate()
		# credit
		credit_row = journal_entry.append("accounts", {})
		credit_row.party_type = "Customer"
		credit_row.account = recivable_account
		credit_row.party = self.customer
		credit_row.credit_in_account_currency = flt(
			self.grand_total, precision)
		credit_row.reference_type = self.doctype
		credit_row.reference_name = self.name
		# debit
		debit_row = journal_entry.append("accounts", {})
		debit_row.account = project_account
		debit_row.debit_in_account_currency = flt(self.grand_total, precision)
		debit_row.reference_type = self.doctype
		debit_row.reference_name = self.name
		journal_entry.save()
		journal_entry.submit()
		form_link = get_link_to_form(journal_entry.doctype, journal_entry.name)
		frappe.msgprint("Journal Entry %s Create Successfully" % form_link)

		# second journal
		s_journal_entry = frappe.new_doc('Journal Entry')
		s_journal_entry.company = company
		s_journal_entry.posting_date = nowdate()
		# credit
		s_credit_row = s_journal_entry.append("accounts", {})
		s_credit_row.account = cash_account
		s_credit_row.credit_in_account_currency = flt(
			self.grand_total, precision)
		s_credit_row.reference_type = self.doctype
		s_credit_row.reference_name = self.name
		# debit
		s_debit_row = s_journal_entry.append("accounts", {})
		s_debit_row.account = recivable_account
		s_debit_row.party_type = "Customer"
		s_debit_row.party = self.customer
		s_debit_row.debit_in_account_currency = flt(
			self.grand_total, precision)
		s_debit_row.reference_type = self.doctype
		s_debit_row.reference_name = self.name
		s_journal_entry.save()
		form_link = get_link_to_form(journal_entry.doctype, journal_entry.name)
		frappe.msgprint("Journal Entry %s Create Successfully" % form_link)
		# self.paid=1
		# self.save()
		frappe.db.sql(
			"""update tabClearance set paid=1 where name='%s'""" % self.name)
		frappe.db.commit()

	@frappe.whitelist()
	def can_create_invoice(self, doctype):
		invoice = frappe.db.get_value(
			doctype, {"clearance": self.name, "docstatus": ["<", 2]}, 'name')
		return 0 if invoice else 1

	def create_deduction_je(self):
		if getattr(self, 'deductions') and self.total_deductions:
			if self.clearance_type == "incoming":
				if not self.purchase_order:
					frappe.throw(_("Please set Purchase Order"))
				if not self.supplier:
					frappe.throw(_("Please set Supplier"))
				self.create_deduction_supplier_je()
			if self.clearance_type == "Outcoming":
				if not self.sales_order:
					frappe.throw(_("Please set Sales Order"))
				if not self.customer:
					frappe.throw(_("Please set Customer"))
				self.create_deduction_customer_je()

	def create_deduction_supplier_je(self):
		je = frappe.new_doc("Journal Entry")
		je.posting_date = nowdate()
		je.voucher_type = 'Journal Entry'
		je.company = self.company
		je.remark = f'Deduction against  Supplier {self.supplier} Deduction: ' + \
			self.doctype + " " + self.name
		supplier_account = get_party_account(
			"Supplier", self.supplier, self.company)
		if not supplier_account:
			frappe.throw(
				_("Please Account for supplier {}").format(self.supplier))

		je.append("accounts", {
			"account": supplier_account,
			"account_currency": get_account_currency(supplier_account),
			"debit_in_account_currency": flt(self.total_deductions or 0),
			"party_type": "Supplier",
			"party": self.supplier,
			"reference_type": self.doctype,
			"reference_name": self.name
		})
		for row in self.deductions:
			je.append("accounts", {
				"account": row.account,
				"account_currency": get_account_currency(row.account),
				"credit_in_account_currency": row.amount,
				"cost_center": row.cost_center,
				"project": self.project,
				"reference_type": self.doctype,
				"reference_name": self.name
			})
		je.submit()

	def create_deduction_customer_je(self):
		je = frappe.new_doc("Journal Entry")
		je.posting_date = nowdate()
		je.voucher_type = 'Journal Entry'
		je.company = self.company
		je.remark = f'Deduction against  Customer {self.customer} Deduction: ' + \
			self.doctype + " " + self.name
		customer_account = get_party_account(
			"Customer", self.customer, self.company)
		if not customer_account:
			frappe.throw(
				_("Please Account for Customer {}").format(self.customer))

		je.append("accounts", {
			"account": customer_account,
			"account_currency": get_account_currency(customer_account),
			"credit_in_account_currency": flt(self.total_deductions or 0),
			"party_type": "Customer",
			"party": self.customer,
			"project": self.project,
			"reference_type": self.doctype,
			"reference_name": self.name
		})
		for row in self.deductions:
			je.append("accounts", {
				"account": row.account,
				"account_currency": get_account_currency(row.account),
				"debit_in_account_currency": row.amount,
				"project": self.project,
				"reference_type": self.doctype,
				"reference_name": self.name
			})
		je.submit()

	def update_purchase_order(self, cancel=False):
		if self.purchase_order and self.items and self.clearance_type == "incoming":
			for item in self.items:
				try:
					purchase_order_item = frappe.get_doc(
						"Purchase Order Item", item.purchase_order_item)
					if cancel:
						purchase_order_item.completed_qty -= item.current_qty
					else:
						purchase_order_item.completed_qty += item.current_qty

					purchase_order_item.completed_percent = (
						float(purchase_order_item.completed_qty) / float(purchase_order_item.qty)) * 100
					purchase_order_item.completed_amount = (
						float(purchase_order_item.rate) * float(purchase_order_item.completed_qty))

					if cancel:
						purchase_order_item.remaining_qty = max(
							purchase_order_item.qty, purchase_order_item.qty - purchase_order_item.completed_qty)
					else:
						purchase_order_item.remaining_qty = min(
							0, purchase_order_item.qty - purchase_order_item.completed_qty)

					purchase_order_item.remaining_percent = (
						float(purchase_order_item.remaining_qty) / float(purchase_order_item.qty)) * 100
					purchase_order_item.remaining_amount = (
						float(purchase_order_item.rate) * float(purchase_order_item.remaining_qty))
					purchase_order_item.save()
				except:
					pass


@frappe.whitelist()
def get_item_price(comparison, item_code, clearance_state, qty):
	comparison_doc = frappe.get_doc("Comparison", comparison)
	if comparison_doc:
		items = [
			x for x in comparison_doc.item if x.clearance_item == item_code]
		item_price = 0 if not len(items) else items[0].price
		state_percent = 0
		if comparison_doc.tender:
			tender = frappe.get_doc("Tender", comparison_doc.tender)
			states_template = [
				x for x in tender.states_template if x.state == clearance_state]
			state_percent = 0 if not len(states_template) else states_template[0].percent
			# total_qty = sum([x.qty for x in items]) or 1
			# item_price = item_price * (((flt(qty)/total_qty) * state_percent)/100)

		return {
			"state_percent": state_percent,
			"item_price": item_price
		}


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_state_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select state from `tabTender States Template`
		where parent = %(parent)s and state like %(txt)s
		limit %(start)s, %(page_len)s""", {
			'parent': filters.get("parent"),
			'start': start,
			'page_len': page_len,
			'txt': "%%%s%%" % txt
		})
















@frappe.whitelist()
def clearance_make_purchase_invoice(source_name, target_doc=None):
    doc = frappe.get_doc("Clearance", source_name)
    invoice = make_purchase_invoice(doc.purchase_order)
    invoice.set_missing_values()
    invoice.is_contracting = 1
    invoice.clearance = doc.name
    invoice.comparison = doc.comparison
    # invoice.set("items",[])
    for row in doc.items:
        invoice_item = [
            x for x in invoice.items if x.po_detail == row.purchase_order_item]
        if len(invoice_item) > 0:
            invoice_item = invoice_item[0]
            invoice_item.qty = row.current_qty

    try:
        invoice.save(ignore_permissions=1)
    except Exception as e:
        frappe.throw(str(e))
    # invoice.submit()
    # doc.purchase_invoice = pi.name
    # doc.save()
    return invoice


@frappe.whitelist()
def clearance_make_sales_invoice(source_name, target_doc=None):
    doc = frappe.get_doc("Clearance", source_name)
    invoice = make_sales_invoice(doc.sales_order)
    invoice.set_missing_values()
    invoice.is_contracting = 1
    invoice.clearance = doc.name
    invoice.comparison = doc.comparison
    for row in doc.items:
        invoice_item = [
            x for x in invoice.items if x.item_code == row.clearance_item]
        if len(invoice_item) > 0:
            invoice_item = invoice_item[0]
            invoice_item.qty = row.current_qty
    try:
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
