# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Clearance(Document):
	def on_submit(self):
		self.update_comparison()
		self.update_purchase_order()
	def on_cancel(self):
		self.update_purchase_order(cancel=1)
	def update_comparison(self):
		if self.comparison and self.items and self.clearance_type == "Outcoming":
			doc = frappe.get_doc("Comparison",self.comparison)
			for clearence_item in self.items:
				for comparison_item in doc.item:
					if clearence_item.clearance_item == comparison_item.clearance_item:
						## set previous qty and completed qty in clearence
						clearence_item.previous_qty       = comparison_item.completed_qty
						clearence_item.completed_qty      = clearence_item.current_qty + clearence_item.previous_qty
						clearence_item.completed_percent  = (float(clearence_item.completed_qty) / float(clearence_item.qty)) *100 if clearence_item.qty else 0
						clearence_item.previous_percent   = (float(clearence_item.previous_qty) / float(clearence_item.qty)) *100 if clearence_item.qty else 0
						clearence_item.previous_amount	  = float(clearence_item.previous_qty) * float(clearence_item.price)

						### update comparison
						comparison_item.completed_qty    += clearence_item.current_qty
						comparison_item.completed_percent = ( comparison_item.completed_qty / clearence_item.qty) *100 if clearence_item.qty else 0
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
	









	def update_purchase_order(self,cancel = False):
		if self.purchase_order and self.items and self.clearance_type == "incoming":
			for item in self.items :
				try : 
					purchase_order_item = frappe.get_doc("Purchase Order Item",item.purchase_order_item)
					if cancel :
						purchase_order_item.completed_qty -= item.qty
					else :
						purchase_order_item.completed_qty += item.qty

					purchase_order_item.completed_percent  = (float(purchase_order_item.completed_qty) / float(purchase_order_item.qty)) *100
					purchase_order_item.completed_amount  = (float(purchase_order_item.rate) * float(purchase_order_item.completed_qty))

					if cancel :
						purchase_order_item.remaining_qty = max(item.qty,item.qty - purchase_order_item.completed_qty)
					else:
						purchase_order_item.remaining_qty = min(0,item.qty - purchase_order_item.completed_qty)

					purchase_order_item.remaining_percent  = (float(purchase_order_item.remaining_qty) / float(purchase_order_item.qty)) *100
					purchase_order_item.remaining_amount  = (float(purchase_order_item.rate) * float(purchase_order_item.remaining_qty))
					purchase_order_item.save()
				except :
					pass

				











