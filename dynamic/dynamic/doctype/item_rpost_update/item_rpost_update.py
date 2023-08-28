# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from  erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import repost_entries

class Itemrpostupdate(Document):
	def on_submit(self):
		self.create_repost()
	
	def create_repost(self) :
		reposted_data = self.get_posted_data()
		for i in reposted_data :
			r = frappe.new_doc("Repost Item Valuation") 
			r.based_on = "Transaction"
			r.voucher_type = self.doctype_list
			r.voucher_no = i.get("voucher_no")
			r.posting_date = i.get("posting_date")
			r.save()
			r.docstatus =1
			r.save()
			self.append_repost_entries(r.name)
			frappe.db.commit()

		repost_entries()

	def append_repost_entries(self , item_name ):	
		self.append("items", {
		"repost_item":item_name,
		})

	def validate(self)  :
		# self.get_posted_data()
		# self.create_repost()
		pass
	def get_posted_data(self)  :

		sql_query = f""" SELECT  a.voucher_no ,a.incoming_rate ,a.posting_date FROM 
		
		`tabStock Ledger Entry` a
		 inner join `tabSales Invoice` b
			ON a.voucher_no = b.name 
		 
		   WHERE item_code = '{self.item}' AND b.docstatus =1
		 
		  and voucher_type  ='{self.doctype_list}' """

		#set value rane for in come value 

		if self.vlaue_range  :
			sql_query = sql_query + f" and incoming_rate > '{self.vlaue_range }'"

		if self.error_value_less_than : 
			sql_query = sql_query + f" and incoming_rate < '{self.error_value_less_than }'"

		# add dcotype filetr 
		data = frappe.db.sql(sql_query ,as_dict=1)
		frappe.msgprint(str(data))
		return data