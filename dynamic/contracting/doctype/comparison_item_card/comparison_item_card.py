# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ComparisonItemCard(Document):
	def on_submit(self):
		self.result = (self.total_item_cost / self.qty)
		doc = frappe.get_doc("Comparison",self.comparison)
		if bool(doc):
			for item in doc.item :
				if item.clearance_item == self.item_code:
					item.price = self.result
					item.total_price = self.result * item.qty
			doc.save()

