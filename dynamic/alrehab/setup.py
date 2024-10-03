import frappe
import os
import json


from frappe import _



def install_elrehab():
	add_properties_journal_auto()

def add_properties_journal_auto():
	name = "Journal Entry Account-reference_type"
	if frappe.db.exists("Property Setter",name) :
		doc = frappe.get_doc("Property Setter",name)
	else :
		doc = frappe.new_doc("Property Setter")
	try:
		doc.doc_type  = "Journal Entry Account"
		doc.doctype_or_field = "DocField"
		doc.field_name = "reference_type"
		doc.name = name
		doc.property = "options"
		doc.property_type = "Text"
		doc.value = "\nSales Invoice\nPurchase Invoice\nJournal Entry\nSales Order\nPurchase Order\nExpense Claim\nAsset\nLoan\nPayroll Entry\nEmployee Advance\nExchange Rate Revaluation\nInvoice Discounting\nFees\nComparison\nClearance\nTender\nPayroll Month\nSubscription\nPayment Entry"
		doc.save()
	except Exception as e:
		frappe.throw(_(str(e)))
