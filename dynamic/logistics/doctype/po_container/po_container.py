# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff , now
from frappe import _
DOMAINS = frappe.get_active_domains()

class POContainer(Document):
	@frappe.whitelist()
	def get_purchase_order_details(self ,purchase_order):
		if purchase_order :
			purchase_order = frappe.get_value(
               "Purchase Order", purchase_order, ["supplier", "grand_total"], as_dict=1)
			return purchase_order.get("supplier") , purchase_order.get("grand_total")
	
	@frappe.whitelist()
	def fetch_purchase_order_items(self):
		if self.items :
			self.items = []

		conditions = " PO.name in ("
		for purchase_order_container in self.purchase_order_containers:
				conditions += f"'{purchase_order_container.purchase_order}' ,"
		conditions = conditions[:len(conditions)-1]
		conditions += ")"
		sql = f'''
			SELECT 
				PO.name as purchase_order, POI.item_code as item , POI.qty , POI.name as row_name
			FROM 
				`tabPurchase Order` PO
			INNER JOIN
				`tabPurchase Order Item` POI
			ON 
				PO.name = POI.parent
			WHERE 
				{conditions}
				'''
		data = frappe.db.sql(sql , as_dict = 1)
		for row in data :
			self.append("items" , row)
		
	@frappe.whitelist()
	def change_status(self):
		self.db_set("status", "Delivered")

	@frappe.whitelist()
	def close_request_item(self):
		if 'Logistics' in DOMAINS: 
			for purchase_order_container in self.purchase_order_containers:
				frappe.db.set_value('Purchase Order',purchase_order_container.purchase_order,'has_delivered','1')
		
	@frappe.whitelist()
	def filter_items(self , purchase_order):
		list = []
		sql = f'''
			SELECT 
			 	POI.item_code
			FROM 
				`tabPurchase Order` PO
			INNER JOIN
				`tabPurchase Order Item` POI
			ON 
				PO.name = POI.parent
			WHERE 
				PO.name = '{purchase_order}'
			'''
		data = frappe.db.sql(sql , as_dict = 1)
		for row in data :
			list.append(row["item_code"])
		return list
	
	@frappe.whitelist()
	def get_items_qty(self , item , purchase_order):
		sql = f'''
			SELECT 
			 	POI.qty , POI.name
			FROM 
				`tabPurchase Order` PO
			INNER JOIN
				`tabPurchase Order Item` POI
			ON 
				PO.name = POI.parent
			WHERE 
				PO.name = '{purchase_order}' 
				and 
				POI.item_code = '{item}'
			'''
		data = frappe.db.sql(sql , as_dict = 1)
		return data[0]["qty"] , data[0]["name"] 
	
	def before_validate(self):
		if 'Logistics' in DOMAINS: 
			self.validate_item_qty()
				
	def before_submit(self):
		if 'Logistics' in DOMAINS: 
			self.calculate_remaining_date()

	def before_cancel(self):
		if 'Logistics' in DOMAINS:
			self.update_shipped_qty()

	def update_shipped_qty(self):
		for item in self.items :
			if item.row_name :
				shipped_qty = frappe.get_value("Purchase Order Item" , item.row_name,'shipped_qty')
				frappe.db.set_value('Purchase Order Item',item.row_name,'shipped_qty',(shipped_qty -item.qty))

	def validate_item_qty(self):
		for item in self.items:
			if (item.row_name):
				doc=frappe.get_list("Purchase Order Item", 
						filters={"parenttype": "Purchase Order",
			   					"parent":item.purchase_order , "name" : item.row_name},
						fields=["qty" , "shipped_qty"])
				if item.qty > (doc[0]["qty"] - doc[0]["shipped_qty"]):
					frappe.throw(_(f"Qty is bigger than qty in purchase order in row {item.idx} , avaliable only {(doc[0]['qty'] - doc[0]['shipped_qty'])}"))

	def set_shipped_qty_of_purchase_order(self) :
		for item in self.items :
			if item.row_name :
				shipped_qty = frappe.get_value("Purchase Order Item" , item.row_name,'shipped_qty')
				frappe.db.set_value('Purchase Order Item',item.row_name,'shipped_qty',shipped_qty + item.qty)
				frappe.db.set_value('Purchase Order',item.purchase_order,'has_shipped','1')
	
	def calculate_remaining_date(self):
		differance = date_diff( self.arrived_date ,now() )
		self.remaining_date = f'{differance}' + " days"
		self.set_shipped_qty_of_purchase_order()