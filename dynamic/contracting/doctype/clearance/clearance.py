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
			print("from iffffff")
			for clearence_item in self.items:
				print("from f iffffffffffff")
				for comparison_item in doc.item:
					print("from second iffffffffffff")
					if clearence_item.clearance_item == comparison_item.clearance_item:
						print("from equal ifff")
						## set previous qty and completed qty in clearence
						clearence_item.previous_qty       = comparison_item.completed_qty
						clearence_item.completed_qty      = clearence_item.current_qty
						clearence_item.completed_percent  = (float(clearence_item.completed_qty) / float(clearence_item.qty)) *100
						clearence_item.previous_percent   = (float(clearence_item.previous_qty) / float(clearence_item.qty)) *100
						clearence_item.previous_amount	  = float(clearence_item.previous_qty) * float(clearence_item.price)

						### update comparison
						comparison_item.completed_qty    += clearence_item.current_qty
						print("comparison_item.completed_qty",comparison_item.completed_qty)
						comparison_item.completed_percent = ( comparison_item.completed_qty / clearence_item.qty) *100
						comparison_item.remaining_qty	  = clearence_item.qty - comparison_item.completed_qty
						comparison_item.remaining_percent = (comparison_item.remaining_qty / comparison_item.qty) * 100
						comparison_item.remaining_amount  = float(comparison_item.remaining_qty) * float(clearence_item.price)

						### update remaining in clearence
						clearence_item.remaining_qty = clearence_item.qty - comparison_item.completed_qty
						clearence_item.remaining_percent = (comparison_item.remaining_qty / comparison_item.qty) * 100
						clearence_item.remaining_amount = float(comparison_item.remaining_qty) * float(clearence_item.price)

			self.save()
			doc.save()
		else:
			pass
