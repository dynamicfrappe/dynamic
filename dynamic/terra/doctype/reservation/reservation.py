# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Reservation(Document):
	def validate(self):
		pass


	
	def check_available_ietm_in_stock(self):
		pass	