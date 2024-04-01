# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockReservationEntry(Document):
	def on_change(self):
		  validation(self)
	


@frappe.whitelist()
def validation(doc):
	if float(doc.delivered_qty or 0 ) < 0:
		doc.delivered_qty = 0
	if float(doc.reserved_qty or 0) < 0 :
		doc.reserved_qty = 0
	
	if doc.delivered_qty is None or doc.delivered_qty == 0:
		delivered_qty = 0
		if float(delivered_qty) >= float(doc.reserved_qty):
			doc.status = "Delivered"
		elif delivered_qty > 0 and doc.delivered_qty < doc.reserved_qty:
			doc.status = "Partially Delivered"
		elif delivered_qty <= 0:
			doc.status = "Reserved"

	else: 
		if doc.delivered_qty >= doc.reserved_qty:
			doc.status = "Delivered"
		elif doc.delivered_qty > 0 and doc.delivered_qty < doc.reserved_qty:
			doc.status = "Partially Delivered"
		elif doc.delivered_qty <= 0:
			doc.status = "Reserved"
	
	if float(doc.delivered_qty or 0 )  > float(doc.reserved_qty):
		doc.delivered_qty = doc.reserved_qty
	
	# if doc.delivered_qty < 0 or doc.delivered_qty < 0 :
	# 	frappe.throw("Error Qty")
	doc.db_update()

