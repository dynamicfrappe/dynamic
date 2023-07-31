


import frappe
from frappe import _
from erpnext.accounts.doctype.payment_entry.payment_entry import (
	set_party_type,set_party_account,set_payment_type
,set_party_account_currency,set_grand_total_and_outstanding_amount,get_bank_cash_account,set_paid_amount_and_received_amount
,apply_early_payment_discount,get_party_bank_account,get_reference_as_per_payment_terms
,split_early_payment_discount_loss,set_pending_discount_loss
)
from frappe import ValidationError, _, scrub, throw
from frappe.utils import cint, comma_or, flt, get_link_to_form, getdate, nowdate
from functools import reduce



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

			for reference in get_reference_as_per_payment_terms(
				doc.payment_schedule, dt, dn, doc, grand_total, outstanding_amount, party_account_currency
			):
				# frappe.throw('test1')
				pe.append("references", reference)
		else:
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