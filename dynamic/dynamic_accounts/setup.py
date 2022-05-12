import frappe
import os
import json





def install_dynamic_accounts():
    add_properties()
   




def add_properties():
	return
	try:
		name = "Journal Entry Account-reference_type-options"
		if frappe.db.exists("Property Setter",name) :
			doc = frappe.get_doc("Property Setter",name)
		else :

			doc = frappe.new_doc("Property Setter")

		doc.doc_type  = "Journal Entry Account"
		doc.doctype_or_field = "DocField"
		doc.field_name = "reference_type"
		doc.name = name
		doc.property = "options"
		doc.property_type = "Text"
		doc.value = "\nSales Invoice\nPurchase Invoice\nJournal Entry\nSales Order\nPurchase Order\nExpense Claim\nAsset\nLoan\nPayroll Entry\nEmployee Advance\nExchange Rate Revaluation\nInvoice Discounting\nFees\nPay and Receipt Document\nComparison\nClearance\nTender"

		doc.save()
	except:
		pass
	try:
		doc = frappe.new_doc("Pay and Receipt Type")
		doc.type = 'Pay'
		doc.save()
	except:
		pass

	try:
		doc = frappe.new_doc("Pay and Receipt Type")
		doc.type = 'Receive'
		doc.save()
	except:
		pass



