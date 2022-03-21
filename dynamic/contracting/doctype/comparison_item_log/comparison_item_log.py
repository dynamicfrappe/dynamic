# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import now_datetime

class ComparisonItemLog(Document):
	def validate(self):
		self.set_missing_values()
		self.set_pervious_qty()
		self.update_statistics_values()
	
	def set_missing_values(self):
		sql = f"""
		select * from `tabComparison Item` where clearance_item = '{self.item_code}' and parent = '{self.comparison}'
		"""
		comparison_item = frappe.db.sql(sql,as_dict=1)
		if comparison_item :
			comparison_item=comparison_item[0]

		self.total_qty = 0 if not comparison_item else comparison_item.qty
		self.comparison_price = 0 if not comparison_item else comparison_item.price
	

		self.posting_date = now_datetime()
		self.current_qty = self.qty or self.current_qty or 0
		self.current_amount = self.price * self.current_qty
		self.current_percent = (self.current_qty or 0) /( self.total_qty or 1)
		

	def update_statistics_values(self):
		self.completed_qty = self.current_qty + self.pervious_qty
		self.completed_amount = self.current_amount + self.pervious_amount
		self.completed_percent = self.current_percent + self.pervious_percent



		self.remaining_qty = max((self.total_qty - self.completed_qty),0)
		self.remaining_amount = self.remaining_qty * self.price
		self.remaining_percent = max((100 - self.completed_percent),0)



	def set_pervious_qty(self):
		sql = f"""
		select  SUM(IFNULL(current_qty,0)) as current_qty,
		 		SUM(IFNULL(current_amount,0)) as current_amount 
		from `tabComparison Item Log`
		where item_code = '{self.item_code}' and state ='{self.state}' and docstatus =1 
		and comparison = '{self.comparison}'
		
		"""
		result = frappe.db.sql(sql,as_dict=1)
		if result :
			result = result[0]
		
		self.pervious_qty = 0 if not result else (result.current_qty or 0)
		self.pervious_amount = 0 if not result else (result.current_amount or 0)
		self.pervious_percent = (self.pervious_qty or 0) / (self.total_qty or 1) * 100


						#log = frappe.new_doc("Comparison Item Log")
						# log.posting_date = now_datetime()
						# log.state = clearence_item.clearance_state
						# log.state_percent = clearence_item.state_percent
						# log.item_code = clearence_item.clearance_item
						# log.item_name = clearence_item.clearance_item_name
						# log.description = clearence_item.clearance_item_description
						# log.uom = clearence_item.uom
						# log.qty = clearence_item.current_qty or 0
						# log.total_qty = comparison_item.qty or 0
						# log.price = clearence_item.current_price or 0
						# log.current_amount = completed_amount
						# log.current_percent = completed_percent
						# log.comparison = doc.name
						# log.reference_type = self.doctype
						# log.reference_name = self.name
						# log.submit()