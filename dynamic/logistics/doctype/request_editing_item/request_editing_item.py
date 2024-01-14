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
			if (not actual_qty) :
				frappe.throw(_("Item '{0}' not exist in '{1}'").format(item_code , warehouse))
			if actual_qty[0]["actual_qty"] == 0.0 :
				frappe.throw(_("Actual Qty of Item '{0}' is '{1}'").format(item_code , actual_qty[0]["actual_qty"] ))
			return float(actual_qty[0]["actual_qty"])
	
			
	def on_submit(self) :
		if not self.approve and not self.rejected		 :
			frappe.throw(_("Can not submit without approve or reject !"))
		if self.approve and not self.approve_by :
			frappe.throw(_("please Set Approved By "))
		if self.rejected and not self.rejected_by :
			frappe.throw(_("please Set Rejected By ! "))