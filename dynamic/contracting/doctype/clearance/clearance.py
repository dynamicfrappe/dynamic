# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Clearance(Document):
	def on_submit(self):
		self.update_comparison()
	def update_comparison(self):
		if self.comparison and self.items and self.clearance_type == "Outcoming":
			doc = frappe.get_doc("Comparison",self.comparison)

			for clearence_item in self.items:
				for comparison_item in doc.item:
					if clearence_item.clearance_item == comparison_item.clearance_item:
						## set previous qty and completed qty in clearence
						clearence_item.previous_qty       = comparison_item.completed_qty
						clearence_item.completed_qty      = clearence_item.current_qty
						comparison_item.completed_qty    += clearence_item.current_qty
						comparison_item.completed_percent = (clearence_item.current_qty / comparison_item.completed_qty) *100
						comparison_item.remaining_qty	  = clearence_item.qty - comparison_item.completed_qty
						comparison_item.remaining_percent = (comparison_item.remaining_qty / comparison_item.qty) * 100
						comparison_item.remaining_amount  = float(comparison_item.remaining_qty) * float(clearence_item.price)
			doc.save()
		else:
			pass
