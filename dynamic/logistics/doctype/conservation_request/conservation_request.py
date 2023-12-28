# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ConservationRequest(Document):
	@frappe.whitelist()
	def get_warranties(self , serial_number):
		item = frappe.db.get_value('Serial No', serial_number ,["item_code", "warranty_expiry_date"], as_dict=1)

		item_code = frappe.get_value(
               "Item", item.get("item_code"), ["item_name", "description"], as_dict=1)
		return item.get("item_code") ,item_code.get("item_name") , item_code.get("description") ,item.get("warranty_expiry_date")
