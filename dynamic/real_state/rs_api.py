


import frappe
from frappe import _
from erpnext.accounts.doctype.payment_entry.payment_entry import (
		set_party_type,set_party_account,set_payment_type
	,set_party_account_currency,set_grand_total_and_outstanding_amount,get_bank_cash_account,set_paid_amount_and_received_amount
	,apply_early_payment_discount,get_party_bank_account,get_reference_as_per_payment_terms

	)
try :
	from erpnext.accounts.doctype.payment_entry.payment_entry import 	split_early_payment_discount_loss ,set_pending_discount_loss
except :
	from .utils import split_early_payment_discount_loss ,set_pending_discount_loss

from frappe import ValidationError, _, scrub, throw
from frappe.utils import cint, comma_or, flt, get_link_to_form, getdate, nowdate
from functools import reduce
import pandas as pd


DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def create_first_contract(source_name):
	item_doc = frappe.get_doc("Item",source_name)
	new_quotation = frappe.new_doc("Quotation")
	new_quotation.append('items',{
		'item_code':item_doc.name,
		'item_name':item_doc.item_name,
		'uom':item_doc.stock_uom,
		'qty':1,
	})
	return new_quotation
	



@frappe.whitelist()
def get_payment_entry(
	dt,
	dn,
	party_amount=None,
	bank_account=None,
	bank_amount=None,
	reference_date=None,
):
	# frappe.throw('get_new_one tra tra')
	# frappe.throw('test1')
	reference_doc = None
	doc = frappe.get_doc(dt, dn)
	if dt in ("Sales Order", "Purchase Order") and flt(doc.per_billed, 2) > 0:
		frappe.throw(_("Can only make payment against unbilled {0}").format(dt))

	party_type = set_party_type(dt)
	party_account = set_party_account(dt, dn, doc, party_type)
	party_account_currency = set_party_account_currency(dt, party_account, doc)
	payment_type = set_payment_type(dt, doc)
	grand_total, outstanding_amount = set_grand_total_and_outstanding_amount(
		party_amount, dt, party_account_currency, doc
	)

	# bank or cash
	bank = get_bank_cash_account(doc, bank_account)

	paid_amount, received_amount = set_paid_amount_and_received_amount(
		dt, party_account_currency, bank, outstanding_amount, payment_type, bank_amount, doc
	)

	reference_date = getdate(reference_date)
	paid_amount, received_amount, discount_amount, valid_discounts = apply_early_payment_discount(
		paid_amount, received_amount, doc, party_account_currency, reference_date
	)

	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = payment_type
	pe.company = doc.company
	pe.cost_center = doc.get("cost_center")
	pe.posting_date = nowdate()
	pe.reference_date = reference_date
	pe.mode_of_payment = doc.get("mode_of_payment")
	pe.party_type = party_type
	pe.party = doc.get(scrub(party_type))
	pe.contact_person = doc.get("contact_person")
	pe.contact_email = doc.get("contact_email")
	pe.ensure_supplier_is_not_blocked()

	pe.paid_from = party_account if payment_type == "Receive" else bank.account
	pe.paid_to = party_account if payment_type == "Pay" else bank.account
	pe.paid_from_account_currency = (
		party_account_currency if payment_type == "Receive" else bank.account_currency
	)
	pe.paid_to_account_currency = (
		party_account_currency if payment_type == "Pay" else bank.account_currency
	)
	pe.paid_amount = paid_amount
	pe.received_amount = received_amount
	pe.letter_head = doc.get("letter_head")

	if dt in ["Purchase Order", "Sales Order", "Sales Invoice", "Purchase Invoice"]:
		pe.project = doc.get("project") or reduce(
			lambda prev, cur: prev or cur, [x.get("project") for x in doc.get("items")], None
		)  # get first non-empty project from items

	if pe.party_type in ["Customer", "Supplier"]:
		bank_account = get_party_bank_account(pe.party_type, pe.party)
		pe.set("bank_account", bank_account)
		pe.set_bank_account_data()

	# only Purchase Invoice can be blocked individually
	if doc.doctype == "Purchase Invoice" and doc.invoice_is_blocked():
		frappe.msgprint(_("{0} is on hold till {1}").format(doc.name, doc.release_date))
	else:
		if doc.doctype in ("Sales Invoice", "Purchase Invoice","Sales Order") and frappe.get_value(
			"Payment Terms Template",
			{"name": doc.payment_terms_template},
			"allocate_payment_based_on_payment_terms",
		):
			# frappe.throw('tes11')
			for reference in get_reference_as_per_payment_terms_for_real_state(
				doc.payment_schedule, dt, dn, doc, grand_total, outstanding_amount, party_account_currency
			):
				# frappe.throw('test1')
				pe.append("references", reference)
		else:
			# frappe.throw('test333')
			if dt == "Dunning":
				pe.append(
					"references",
					{
						"reference_doctype": "Sales Invoice",
						"reference_name": doc.get("sales_invoice"),
						"bill_no": doc.get("bill_no"),
						"due_date": doc.get("due_date"),
						"total_amount": doc.get("outstanding_amount"),
						"outstanding_amount": doc.get("outstanding_amount"),
						"allocated_amount": doc.get("outstanding_amount"),
					},
				)
				pe.append(
					"references",
					{
						"reference_doctype": dt,
						"reference_name": dn,
						"bill_no": doc.get("bill_no"),
						"due_date": doc.get("due_date"),
						"total_amount": doc.get("dunning_amount"),
						"outstanding_amount": doc.get("dunning_amount"),
						"allocated_amount": doc.get("dunning_amount"),
					},
				)
			else:
				# frappe.throw('test2')
				pe.append(
					"references",
					{
						"reference_doctype": dt,
						"reference_name": dn,
						"bill_no": doc.get("bill_no"),
						"due_date": doc.get("due_date"),
						"total_amount": grand_total,
						"outstanding_amount": outstanding_amount,
						"allocated_amount": outstanding_amount,
						# "payment_term": outstanding_amount,
					},
				)

	pe.setup_party_account_field()
	pe.set_missing_values()

	if party_account and bank:
		if dt == "Employee Advance":
			reference_doc = doc
		pe.set_exchange_rate(ref_doc=reference_doc)
		pe.set_amounts()

		if discount_amount:
			base_total_discount_loss = 0
			if frappe.db.get_single_value("Accounts Settings", "book_tax_discount_loss"):
				base_total_discount_loss = split_early_payment_discount_loss(pe, doc, valid_discounts)

			set_pending_discount_loss(
				pe, doc, discount_amount, base_total_discount_loss, party_account_currency
			)

		pe.set_difference_amount()

	return pe

def set_grand_total_and_outstanding_amount(party_amount, dt, party_account_currency, doc):
	grand_total = outstanding_amount = 0
	if party_amount:
		grand_total = outstanding_amount = party_amount
	elif dt in ("Sales Invoice", "Purchase Invoice"):
		if party_account_currency == doc.company_currency:
			grand_total = doc.base_rounded_total or doc.base_grand_total
		else:
			grand_total = doc.rounded_total or doc.grand_total
		outstanding_amount = doc.outstanding_amount
	elif dt in ("Expense Claim"):
		grand_total = doc.total_sanctioned_amount + doc.total_taxes_and_charges
		outstanding_amount = doc.grand_total - doc.total_amount_reimbursed
	elif dt == "Employee Advance":
		grand_total = flt(doc.advance_amount)
		outstanding_amount = flt(doc.advance_amount) - flt(doc.paid_amount)
		if party_account_currency != doc.currency:
			grand_total = flt(doc.advance_amount) * flt(doc.exchange_rate)
			outstanding_amount = (flt(doc.advance_amount) - flt(doc.paid_amount)) * flt(doc.exchange_rate)
	elif dt == "Fees":
		grand_total = doc.grand_total
		outstanding_amount = doc.outstanding_amount
	elif dt == "Dunning":
		grand_total = doc.grand_total
		outstanding_amount = doc.grand_total
	elif dt == "Donation":
		grand_total = doc.amount
		outstanding_amount = doc.amount
	elif dt == "Gratuity":
		grand_total = doc.amount
		outstanding_amount = flt(doc.amount) - flt(doc.paid_amount)
	elif dt == 'Sales Order':
		grand_total = doc.grand_total
		if doc.payment_schedule:
			paid_amount=0
			for row in doc.payment_schedule:
				paid_amount += row.paid_amount
		outstanding_amount = flt(doc.grand_total) - flt(paid_amount)
	else:
		if party_account_currency == doc.company_currency:
			grand_total = flt(doc.get("base_rounded_total") or doc.base_grand_total)
		else:
			grand_total = flt(doc.get("rounded_total") or doc.grand_total)
		outstanding_amount = grand_total - flt(doc.advance_paid)
	return grand_total, outstanding_amount


@frappe.whitelist()
def so_on_submit(self,*args , **kwargs):
	if 'Real State' in DOMAINS:
		update_against_document_in_jv(self)
		


#?same function but not same cjild field table name
def update_against_document_in_jv(self):
		"""
		Links invoice and advance voucher:
				1. cancel advance voucher
				2. split into multiple rows if partially adjusted, assign against voucher
				3. submit advance voucher
		"""
		from erpnext.accounts.party import get_party_account
		debit_to = get_party_account('Customer',self.customer,self.company)
		total_advance = sum(row.advance_amount for row in self.advancess)
		outstanding_amount =  self.base_grand_total - total_advance

		if self.doctype == "Sales Invoice":
			party_type = "Customer"
			party = self.customer
			party_account = self.debit_to
			dr_or_cr = "credit_in_account_currency"
		elif self.doctype == "Sales Order":
			party_type = "Customer"
			party = self.customer
			party_account = debit_to
			dr_or_cr = "credit_in_account_currency"
		else:
			party_type = "Supplier"
			party = self.supplier
			party_account = self.credit_to
			dr_or_cr = "debit_in_account_currency"

		lst = []
		for d in self.get("advancess"):
			if flt(d.allocated_amount) > 0:
				args = frappe._dict(
					{
						"voucher_type": d.reference_type,
						"voucher_no": d.reference_name,
						"voucher_detail_no": d.reference_row,
						"against_voucher_type": self.doctype,
						"against_voucher": self.name,
						"account": party_account,
						"party_type": party_type,
						"party": party,
						"is_advance": "Yes",
						"dr_or_cr": dr_or_cr,
						"unadjusted_amount": flt(d.advance_amount),
						"allocated_amount": flt(d.allocated_amount),
						"precision": d.precision("advance_amount"),
						"exchange_rate": (
							self.conversion_rate if self.party_account_currency != self.company_currency else 1
						),
						"grand_total": (
							self.base_grand_total
							if self.party_account_currency == self.company_currency
							else self.grand_total
						),
						"outstanding_amount": outstanding_amount, #**self.outstanding_amount,
						"difference_account": frappe.db.get_value(
							"Company", self.company, "exchange_gain_loss_account"
						),
						"exchange_gain_loss": flt(d.get("exchange_gain_loss")),
					}
				)
				lst.append(args)

		if lst:
			from erpnext.accounts.utils import reconcile_against_document

			reconcile_against_document(lst)


def get_reference_as_per_payment_terms_for_real_state(
	payment_schedule, dt, dn, doc, grand_total, outstanding_amount, party_account_currency
):
	# frappe.throw('geeeee888')
	references = []
	is_multi_currency_acc = (doc.currency != doc.company_currency) and (
		party_account_currency != doc.company_currency
	)

	for payment_term in payment_schedule:
		payment_term_outstanding = flt(
			payment_term.payment_amount - payment_term.paid_amount, payment_term.precision("payment_amount")
		)
		if not is_multi_currency_acc:
			# If accounting is done in company currency for multi-currency transaction
			payment_term_outstanding = flt(
				payment_term_outstanding * doc.get("conversion_rate"), payment_term.precision("payment_amount")
			)

		if payment_term_outstanding:
			references.append(
				{
					"reference_doctype": dt,
					"reference_name": dn,
					"bill_no": doc.get("bill_no"),
					"due_date": payment_term.get("due_date"),
					"total_amount": grand_total,
					"outstanding_amount": outstanding_amount,
					"payment_term": payment_term.payment_term,
					"allocated_amount": payment_term_outstanding,
				}
			)

	return references

@frappe.whitelist()
def add_year_date(trans_date):
	d1 = frappe.utils.add_years(trans_date,3)
	return d1


@frappe.whitelist()
def add_template_terms(file):
	pat = file.split('/')
	usecols = ['template','descrption','portion','due_date','month']#,'Serial No','Batch No'
	# data = pd.read_csv(frappe.get_site_path('private', 'files', str(pat[-1])), usecols=usecols)
	#!---
	data = pd.read_excel(frappe.get_site_path('private', 'files', str(pat[-1])) ,sheet_name = 0,engine='openpyxl',usecols=usecols)
	data = data.fillna('')
	# print('\n\n\n=data=>',data,'\n\n\n')
	return get_data(data) 


def get_data(data):
	reponse = []
	for  index, row in data.iterrows():
		if row.get('template')  and str(row.get('template')) !='nan':
			payment_term = row.get('template')  if str(row.get('template')) !='nan' and row.get('template') else " "
			invoice_portion =  row.get('portion')  if str(row.get('portion')) !='nan' and row.get('portion') else " "
			due_date_base_on = row.get('due_date')  if str(row.get('due_date')) !='nan' and row.get('due_date') else " "
			credit_months = row.get('month')  if str(row.get('month')) !='nan' and row.get('month') else " "
			description = row.get('descrption') or ''
			obj = {
				"payment_term" :payment_term , 
				"description" : description , 
				"invoice_portion" : invoice_portion ,
				"due_date_base_on" : due_date_base_on ,
				"credit_months" : credit_months ,
				}
			reponse.append(obj)
	return reponse



@frappe.whitelist()
def setup_payment_term_notify():
	if "Real State" in DOMAINS:
		get_payment_terms_tp_pay()


def get_payment_terms_tp_pay():
	alert_payemnt_term_days= frappe.db.get_single_value('Real Estate Sittings', 'alert_payemnt_term_days') or 0
	data = f"""
	select `tabSales Order`.name as document_name,'Sales Order' AS document_type,`tabPayment Schedule`.payment_term,`tabPayment Schedule`.due_date 
	,`tabPayment Schedule`.parent  
	FROM `tabSales Order`
	INNER JOIN `tabPayment Schedule`
	on `tabSales Order`.name=`tabPayment Schedule`.parent
	LEFT OUTER JOIN `tabPayment Entry Reference`
	ON `tabPayment Entry Reference`.reference_name=`tabPayment Schedule`.parent
	AND `tabPayment Entry Reference`.payment_term =`tabPayment Schedule`.payment_term 
	where `tabPayment Entry Reference`.reference_name is null 
	AND `tabSales Order`.docstatus=1 AND `tabSales Order`.payment_terms_template <> ''
	AND DATE_ADD(`tabPayment Schedule`.due_date,Interval {alert_payemnt_term_days} Day)=CURDATE() 
	"""
	data = frappe.db.sql(data,as_dict=1)
	notify_role= frappe.db.get_single_value('Real Estate Sittings', 'role_to_alert')
	if data and notify_role:
		prepare_enque_data(notify_role,data,send_insurance_notify)


def get_user_by_role(role):
	get_all_manger = f"""
	SELECT DISTINCT(has_role.parent),user.email
	FROM
		`tabHas Role` has_role
			LEFT JOIN `tabUser` user
				ON has_role.parent = user.name
	WHERE
		has_role.parenttype = 'User' AND has_role.role='{role}'
	"""
	return frappe.db.sql(get_all_manger,as_dict=1)

def prepare_enque_data(role,data,method):
	get_all_manger = get_user_by_role(role)
	# frappe.errprint(f'data==>{data}')
	# frappe.errprint(f'get_all_manger==>{get_all_manger}')
	if (data and get_all_manger):
		kwargs={
			"get_all_manger":get_all_manger,
			"data":data,
		}
		frappe.enqueue( 
		method=method,
		job_name="send_insurance_notify",
		queue="default", 
		timeout=500, 
		is_async=False, # if this is True, method is run in worker
		now=True, # if this is True, method is run directly (not in a worker) 
		at_front=False, # put the job at the front of the queue
		**kwargs,
	)
		

def send_insurance_notify(**kwargs):
	for row in kwargs.get("data"):
		for admin in kwargs.get("get_all_manger"):
			owner_name = admin.parent
			notif_doc = frappe.new_doc('Notification Log')
			subject =_("Payment Term With Name {0} AND Due Date {1} For Sales Order {2}").format(row.get('payment_term'),row.get('due_date'),row.get('document_name'))
			mail_msg = _("Payment Term With Name {0} AND Due Date {1} For Sales Order {2}").format(row.get('payment_term'),row.get('due_date'),row.get('document_name'))
			notif_doc.subject = subject
			notif_doc.email_content =mail_msg
			notif_doc.for_user = owner_name
			notif_doc.type = "Mention"
			notif_doc.document_type = row.document_type
			notif_doc.document_name = row.document_name
			notif_doc.from_user = frappe.session.user or ""
			notif_doc.insert(ignore_permissions=True)
			frappe.db.commit()
