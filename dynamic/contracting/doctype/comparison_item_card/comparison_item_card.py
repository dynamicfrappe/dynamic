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
					if self.margin_percent and self.margin_percent > 0 :
						self.margin_rate = ( float(self.result) * (float(self.margin_percent or 0) /100))
						# self.result = float(self.result) +  foat(self.margin_rate)
					item.item_cost = self.result
					item.price = self.result + float(self.margin_rate  or 0 )
					item.total_price = item.price * item.qty
			doc.save()
	def validate(self):
		self.validate_qty()
	def validate_qty(self):
		if not self.qty:
			self.qty = 1
		# if self.qty > self.qty_from_comparison:
		# 	frappe.throw("""You Cant Select QTY More Than %s"""%self.qty_from_comparison)


