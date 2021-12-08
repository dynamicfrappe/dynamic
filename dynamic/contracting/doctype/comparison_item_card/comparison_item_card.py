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
	def validate(self):
		self.validate_qty()
	def validate_qty(self):
		if not self.qty:
			self.qty = 1
		if self.qty > self.qty_from_comparison:
			frappe.throw("""You Cant Select QTY More Than %s"""%self.qty_from_comparison)


