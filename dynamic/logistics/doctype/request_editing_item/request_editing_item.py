# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
from frappe import _

class RequestEditingItem(Document):
	@frappe.whitelist()
	def get_item_qty(self ,item_code , warehouse):
		if item_code and warehouse :
			sql = F'''
			SELECT actual_qty 
				FROM `tabBin` 
			WHERE 
				item_code = '{item_code}' 
				AND 
				warehouse = '{warehouse}'
			'''
			actual_qty = frappe.db.sql(sql , as_dict = 1)
			if not actual_qty :
				frappe.throw(("Item '{0}' not exist in '{1}'").format(item_code , warehouse))
			return actual_qty[0]["actual_qty"]
	

	@frappe.whitelist()
	def create_stock_entry(self):
		if self.item_code and self.source_warehouse and self.target_warehouse and (self.main_item or self.spear_part_item):
			stock_entry = frappe.new_doc("Stock Entry")
			stock_entry.stock_entry_type = "Material Transfer"
			stock_entry.from_warehouse = self.source_warehouse
			stock_entry.to_warehouse = self.target_warehouse
			for item in self.main_item:
				stock_entry.append("items" ,{
					"item_code" : item.item_code ,
					"qty" : float(item.reqd_qty)
				})
			for item in self.spear_part_item:
				stock_entry.append("items" ,{
					"item_code" : item.item_code ,
					"qty" : float(item.reqd_qty)
				})
			stock_entry.append("items" ,{
					"item_code" : self.item_code ,
					"qty" : float(1)
				})
			stock_entry.insert()
			stock_entry.submit()

		lnk = get_link_to_form(stock_entry.doctype, stock_entry.name)
		frappe.msgprint(_("{} {} was Created").format(
			stock_entry.doctype, lnk))
		return lnk
			
			
			