import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry  import *
from erpnext.accounts.doctype.payment_entry.payment_entry  import PaymentEntry





def split_early_payment_discount_loss(pe, doc, valid_discounts) -> float:
	"""Split early payment discount into Income Loss & Tax Loss."""
	total_discount_percent = get_total_discount_percent(doc, valid_discounts)

	if not total_discount_percent:
		return 0.0

	base_loss_on_income = add_income_discount_loss(pe, doc, total_discount_percent)
	base_loss_on_taxes = add_tax_discount_loss(pe, doc, total_discount_percent)

	# Round off total loss rather than individual losses to reduce rounding error
	return flt(base_loss_on_income + base_loss_on_taxes, doc.precision("grand_total"))



def set_pending_discount_loss(
	pe, doc, discount_amount, base_total_discount_loss, party_account_currency
):
	# If multi-currency, get base discount amount to adjust with base currency deductions/losses
	if party_account_currency != doc.company_currency:
		discount_amount = discount_amount * doc.get("conversion_rate", 1)

	# Avoid considering miniscule losses
	discount_amount = flt(discount_amount - base_total_discount_loss, doc.precision("grand_total"))

	# Set base discount amount (discount loss/pending rounding loss) in deductions
	if discount_amount > 0.0:
		positive_negative = -1 if pe.payment_type == "Pay" else 1

		# If tax loss booking is enabled, pending loss will be rounding loss.
		# Otherwise it will be the total discount loss.
		book_tax_loss = frappe.db.get_single_value("Accounts Settings", "book_tax_discount_loss")
		account_type = "round_off_account" if book_tax_loss else "default_discount_account"

		pe.set_gain_or_loss(
			account_details={
				"account": frappe.get_cached_value("Company", pe.company, account_type),
				"cost_center": pe.cost_center or frappe.get_cached_value("Company", pe.company, "cost_center"),
				"amount": discount_amount * positive_negative,
			}
		)


PaymentEntry.split_early_payment_discount_loss = split_early_payment_discount_loss
PaymentEntry.set_pending_discount_loss = set_pending_discount_loss