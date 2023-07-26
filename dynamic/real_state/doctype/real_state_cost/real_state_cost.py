# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import erpnext
from erpnext.stock.doctype.landed_cost_voucher.landed_cost_voucher import LandedCostVoucher
from erpnext.controllers.taxes_and_totals import init_landed_taxes_and_totals
from frappe.model.document import Document
from frappe.model.meta import get_field_precision
from frappe.utils import flt
from frappe.utils import cint, flt, round_based_on_smallest_currency_fraction
from erpnext.stock.get_item_details import get_conversion_factor

import erpnext
from erpnext.accounts.doctype.journal_entry.journal_entry import get_exchange_rate


class RealStateCost(LandedCostVoucher):
	def validate(self):
		# self.create_matrial_issue()
		# self.create_matrial_reciept()
		# self.create_gl_landed_cost()
		
		# self.check_mandatory()
		# self.init_landed_taxes_and_totals()
		# self.set_total_taxes_and_charges()
		# if not self.get("items"):
		# 	self.get_items_from_purchase_receipts()

		# self.set_applicable_charges_on_item()
		...
	def after_insert(self):
		self.create_matrial_issue()
		self.create_matrial_reciept()
		...

	def create_matrial_issue(self):
		stock_matial_issue = frappe.new_doc("Stock Entry")
		stock_matial_issue.stock_entry_type = "Material Issue"
		stock_matial_issue.purpose = "Material Issue"
		stock_matial_issue.from_warehouse = self.source_warehouse
		for row in self.items:
			stock_matial_issue.append('items',{
				's_warehouse' :self.source_warehouse,
				'item_code' :row.item_code,
				'qty' :row.qty,
				'basic_rate' :(row.amount / row.qty),
				'expense_account' :self.temporary_account,
			})
		stock_matial_issue.real_state_cost = self.name
		stock_matial_issue.save(ignore_permissions=1)
	
	def create_matrial_reciept(self):
		all_tax = sum(flt(tax.amount)for tax in self.get("taxes"))
		stock_matial_receipt = frappe.new_doc("Stock Entry")
		stock_matial_receipt.stock_entry_type = "Material Receipt"
		stock_matial_receipt.purpose = "Material Receipt"
		stock_matial_receipt.to_warehouse = self.target_warehouse
		for row in self.items:
			stock_matial_receipt.append('items',{
				't_warehouse' :self.target_warehouse,
				'item_code' :row.item_code,
				'qty' :row.qty,
				'basic_rate' :(row.amount / row.qty) + all_tax,
			})
		# print('\n\n\n===>',stock_matial_receipt.__dict__,'\n\n\n--')
		stock_matial_receipt.real_state_cost = self.name
		stock_matial_receipt.save(ignore_permissions=1)

	def create_gl_landed_cost(self):
		from erpnext.accounts.general_ledger import make_gl_entries, make_reverse_gl_entries
		gl_entries = []
		grand_total = self.purchase_receipts[0].grand_total 
		gl_entries.append(
			self.get_gl_dict({
			'company': self.company,
			"account": self.debit_to,#company stock in hand
			"against": self.temporary_account,
			'voucher_type': 'Real State Cost',
			'voucher_no': self.name,
			'debit': self.total_taxes_and_charges + grand_total,
			'credit': 0,
			'debit_in_account_currency': self.total_taxes_and_charges + grand_total,
			'credit_in_account_currency': 0,
			'is_opening': "No",
			'party_type': None,
			'party': None,
			# 'project': data.get("project")
			# 'remarks': data.get("remarks"),
			# 'posting_date': data.posting_date,
			# 'fiscal_year': fiscal_year,
			})
		)
		
		
		gl_entries.append(
			self.get_gl_dict({
			'company': self.company,
			"account": self.debit_to,#company stock in hand
			"against": self.temporary_account,
			'voucher_type': 'Real State Cost',
			'voucher_no': self.name,
			'debit': self.total_taxes_and_charges + grand_total,
			'credit': 0,
			'debit_in_account_currency': self.total_taxes_and_charges + grand_total,
			'credit_in_account_currency': 0,
			'is_opening': "No",
			'party_type': None,
			'party': None,
			# 'project': data.get("project")
			# 'remarks': data.get("remarks"),
			# 'posting_date': data.posting_date,
			# 'fiscal_year': fiscal_year,
			})
		)

		make_gl_entries(
					gl_entries,
					update_outstanding='No',
					merge_entries=False,
					from_repost=False,
				)
		

	def init_landed_taxes_and_totals(self):
		self.tax_field = "taxes" 
		self.set_account_currency()
		self.set_exchange_rate()
		self.set_amounts_in_company_currency()
	
	def set_account_currency(self):
		company_currency = erpnext.get_company_currency(self.company)
		for d in self.get(self.tax_field):
			if not d.account_currency:
				account_currency = frappe.db.get_value("Account", d.expense_account, "account_currency")
				d.account_currency = account_currency or company_currency

	def set_exchange_rate(self):
		company_currency = erpnext.get_company_currency(self.company)
		for d in self.get(self.tax_field):
			if d.account_currency == company_currency:
				d.exchange_rate = 1
			elif not d.exchange_rate:
				d.exchange_rate = get_exchange_rate(
					self.posting_date,
					account=d.expense_account,
					account_currency=d.account_currency,
					company=self.company,
				)

			if not d.exchange_rate:
				frappe.throw(_("Row {0}: Exchange Rate is mandatory").format(d.idx))

	def set_amounts_in_company_currency(self):
		for d in self.get(self.tax_field):
			d.amount = flt(d.amount, d.precision("amount"))
			d.base_amount = flt(d.amount * flt(d.exchange_rate), d.precision("base_amount"))


	def on_submit(self):
		self.update_landed_cost()

	def update_landed_cost(self):
		for d in self.get("purchase_receipts"): 
			doc = frappe.get_doc(d.receipt_document_type, d.receipt_document)
			#? validate qty from each invoice
			# self.validate_asset_qty_and_status(d.receipt_document_type, doc)
			#? set landed cost voucher amount in pr item
			self.set_landed_cost_voucher_amount()
			#? set valuation amount in pr item
			# self.update_valuation_rate(doc,reset_outgoing_rate=False)
			#? db_update will update and save landed_cost_voucher_amount and voucher_amount in PR
			all_tax = sum(flt(tax.amount)for tax in self.get("taxes"))
			for item in doc.get("items"):
				item.basic_rate += all_tax
				item.valuation_rate +=  all_tax
				# print('\n\n\n==<item',item.__dict__,'\n\n\n')
				item.db_update()
			
			#!check
			# frappe.throw('before _update stock ledger')

			for d in self.get("purchase_receipts"):
				doc = frappe.get_doc(d.receipt_document_type, d.receipt_document)
				# update stock & gl entries for cancelled state of PR
				doc.docstatus = 2
				doc.update_stock_ledger()
				doc.make_gl_entries_on_cancel()

				# update stock & gl entries for submit state of PR
				doc.docstatus = 1
				doc.update_stock_ledger()
				doc.make_gl_entries()
				doc.repost_future_sle_and_gle()
	

	# update valuation rate
	def update_valuation_rate(self, doc, reset_outgoing_rate=True):
		"""
		item_tax_amount is the total tax amount applied on that item
		stored for valuation

		TODO: rename item_tax_amount to valuation_tax_amount
		"""
		stock_and_asset_items = []
		# stock_and_asset_items = self.get_stock_items() + self.get_asset_items()

		stock_and_asset_items_qty, stock_and_asset_items_amount = 0, 0
		last_item_idx = 1
		for d in doc.get("items"):
			if d.item_code :#and d.item_code in stock_and_asset_items:
				stock_and_asset_items_qty += flt(d.qty)
				stock_and_asset_items_amount += flt(d.basic_amount)
				last_item_idx = d.idx

		total_valuation_amount = sum(
			flt(d.amount)
			for d in self.get("taxes")
			# if d.category in ["Valuation", "Valuation and Total"]
		)

		valuation_amount_adjustment = total_valuation_amount
		for i, item in enumerate(doc.get("items")):
			if item.item_code and item.qty :#and item.item_code in stock_and_asset_items:
				item_proportion = (
					flt(item.amount) / stock_and_asset_items_amount
					if stock_and_asset_items_amount
					else flt(item.qty) / stock_and_asset_items_qty
				)

				# if i == (last_item_idx - 1):
				# 	item.item_tax_amount = flt(
				# 		valuation_amount_adjustment, self.precision("item_tax_amount", item)
				# 	)
				# else:
				# 	item.item_tax_amount = flt(
				# 		item_proportion * total_valuation_amount, self.precision("item_tax_amount", item)
				# 	)
				# 	valuation_amount_adjustment -= item.item_tax_amount

				doc.round_floats_in(item)
				if flt(item.conversion_factor) == 0.0:
					item.conversion_factor = (
						get_conversion_factor(item.item_code, item.uom).get("conversion_factor") or 1.0
					)

				qty_in_stock_uom = flt(item.qty * item.conversion_factor)
				item.rm_supp_cost = 0.0 # doc.get_supplied_items_cost(item.name, reset_outgoing_rate) or 0
				item.valuation_rate = (
					item.amount
					# + item.item_tax_amount
					+ item.rm_supp_cost
					# + flt(item.landed_cost_voucher_amount)
				) / qty_in_stock_uom
			else:
				item.valuation_rate = 0.0


	def set_landed_cost_voucher_amount(self):
		for d in self.get("items"):
			lc_voucher_data = frappe.db.sql(
				"""select sum(applicable_charges), cost_center
				from `tabLanded Cost Item`
				where docstatus = 1 and purchase_receipt_item = %s""",
				d.name,
			)
			print('\n\n\n===> lc_voucher_data ****',lc_voucher_data,'\n\n')
			d.landed_cost_voucher_amount = lc_voucher_data[0][0] if lc_voucher_data else 0.0
			if not d.cost_center and lc_voucher_data and lc_voucher_data[0][1]:
				print('\n\n\n===> not d.cost_center ##',d.landed_cost_voucher_amount,'\n\n')
				d.db_set("cost_center", lc_voucher_data[0][1])
	"""
	sql deleted : pr_item.cost_center, pr_item.is_fixed_asset
	and exists(select name from tabItem
						where name = pr_item.item_code and (is_stock_item = 1 or is_fixed_asset=1))
	"""
	@frappe.whitelist()
	def get_items_from_purchase_receipts(self):
		self.set("items", [])
		for pr in self.get("purchase_receipts"):
			if pr.receipt_document_type and pr.receipt_document:
				# print('\n\n\n\n===>',pr.receipt_document_type , pr.receipt_document,'\n\n\n\n')
				pr_items = frappe.db.sql(
					"""select 
						pr_item.item_code,
					  	pr_item.description,
						pr_item.qty,
						pr_item.basic_amount,
						pr_item.amount,
						pr_item.item_name
					from `tab{doctype}` pr_item where parent = %s
					""".format(
						doctype='Stock Entry Detail'
					),
					pr.receipt_document,
					as_dict=True,
				)

				for d in pr_items:
					item = self.append("items")
					item.item_code = d.item_code
					item.description = d.description
					item.qty = d.qty
					item.rate = d.basic_amount
					item.cost_center = d.cost_center or erpnext.get_default_cost_center(self.company)
					item.amount = d.amount
					item.receipt_document_type = pr.receipt_document_type
					item.receipt_document = pr.receipt_document
					item.purchase_receipt_item = d.name
					item.is_fixed_asset = d.is_fixed_asset
