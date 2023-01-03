# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from pickle import TRUE
import re
import frappe
from frappe.model.document import Document
from frappe import _ 
class Reservation(Document):

	# def before_insert(self):
	# 	#validate item 
	# 	if not self.item_code :
	# 		frappe .throw(_("Please Select Item First !"))
	# 	# validate required qty 
	# 	if float(self.reservation_amount or 0) == 0 or  float(self.reservation_amount or 0) < 0 :
	# 		frappe.throw(_("Invalid Amount Required "))
	# 	#validate source 
	# 	if  self.warehouse_source and self.order_source :
	# 		frappe.throw(_("Invalid Source "))
	# 	#validate status 
	# 	if self.status == "Active" :
	# 		#validate warehouse case
	# 		if self.warehouse_source :
	# 			self.validate_warehouse()
	# 		if self.order_source :
	# 			self.validate_purchase_order()
	# 		if not self.warehouse_source and not self.order_source:
	# 			frappe.throw(_("Please Select Source As Warehouse Or Purchase Order for Item"))
				# self.get_pur_order_or_warehouse()

		# if self.warehouse:
		# 	self.total_warehouse_reseved()
		# if self.reservation_purchase_order:
		# 	self.total_purchase_order_reseved()
		
	def validate_warehouse(self):
		stock_sql = self.stock_sql()
		if stock_sql and len(stock_sql) > 0 :
			if stock_sql[0].get("qty") == 0 or float( stock_sql[0].get("qty")  or 0 ) < self.reservation_amount  :
				frappe.throw(_(f""" stock value in warehouse {self.warehouse_source} = {stock_sql[0].get("qty")} 
				  and you requires  {self.reservation_amount}  """))
			self.warehouse = [] #?add row
			row = self.append('warehouse', {})
			row.item = self.item_code
			row.bin = stock_sql[0].get("bin") 
			row.warehouse = self.warehouse_source
			row.current_available_qty = stock_sql[0].get("qty") 
			row.reserved_qty = self.reservation_amount
			row.available_qty_atfer___reservation = stock_sql[0].get("qty") - self.reservation_amount
		if  not stock_sql or len(stock_sql) == 0 :
			frappe.throw(_(f""" no stock value in warehouse {self.warehouse_source} for item {self.item_code}  """))

	def stock_sql(self):
		"""get bin which its choosen and check its qty before this transaction and reserv name != self.name"""
		data = frappe.db.sql(f""" 
				      SELECT a.name as bin , 'Bin' as `doctype`,
					CASE 
                         WHEN b.reserved_qty > 0 AND c.status = "Active"
						 then a.actual_qty - SUM(b.reserved_qty)
						 ELSE a.actual_qty 
						 END  as qty
					 FROM 
					`tabBin` a
					LEFT JOIN 
				   `tabReservation Warehouse` b 
					ON a.name = b.bin 
                     LEFT JOIN 
                    `tabReservation` c
                    ON b.parent = c.name
					WHERE a.warehouse = '{self.warehouse_source}'
					AND a.item_code = '{self.item_code}'
                    AND c.name <> "{self.name}"
					
					""" ,as_dict=1)

		return data

	def validate_purchase_order(self):
		order =  frappe.db.sql(f"""                   
										SELECT a.name as `name` ,a.parent,a.parenttype as doctype,
										CASE
										WHEN b.reserved_qty > 0 AND c.status <> "Invalid"
										then (a.qty - a.received_qty) - SUM(b.reserved_qty)
										else a.qty - a.received_qty
										end as qty
										from
										`tabPurchase Order Item` a
										LEFT JOIN
										`tabReservation Purchase Order` b
										ON b.purchase_order_line=a.name 
										LEFT JOIN
										`tabReservation` c
										ON b.parent = c.name AND c.name <> '{self.name}'
										where a.item_code = '{self.item_code}'  and a.parent = '{self.order_source}' 
										""",as_dict=1)
		if order and len(order) > 0 :
			if order[0].get("name") and float(order[0].get("qty")) > 0 :
				# valid = self.validate_order_line(order[0].get("name") , float(order[0].get("qty")))
				if order[0].get('qty') < self.reservation_amount :
					frappe.throw(_(f"Pruchase Order  {self.order_source} = {order[0].get('qty')} and you requires  {self.reservation_amount} "))
				if self.reservation_amount <= order[0].get('qty') :
					# self.add_row_single('pur',order[0])
					self.reservation_purchase_order = [] #?add row
					row = self.append('reservation_purchase_order', {})
					row.item = self.item_code
					row.purchase_order_line = order[0].get("name")
					row.purchase_order = self.order_source
					row.qty = self.reservation_amount
					row.reserved_qty = self.reservation_amount
					row.current_available_qty = float(order[0].get("qty"))
					row.available_qty_atfer___reservation = float(order[0].get("qty")) - self.reservation_amount

			if order[0].get("parent") and float(order[0].get("qty")) ==  0 :
				frappe.throw(_(f"  Purchase Order {self.order_source} don't have {self.item_code} Qty and you requires  {self.reservation_amount}" ))
			if not order[0].get("parent") :
				frappe.throw(_(f"  Purchase Order {self.order_source} don't have item {self.item_code}" ))	
		if not order or  len(order) == 0 :
			frappe.throw(_(f"Invalid Purchase Order {self.order_source} don't have item {self.item_code}"))
	
		


		
	def total_warehouse_reseved(self):
		total_warehouse=0
		for row in self.warehouse:
			total_warehouse += float(row.reserved_qty)
		self.db_set('total_warehouse_reseved_qty',total_warehouse)
	
	def total_purchase_order_reseved(self):
		total_put_order=0
		for row in self.reservation_purchase_order:
			total_put_order += float(row.reserved_qty)
		self.db_set('total_purchase_order_reserved_qty',total_put_order)

	def validate(self):
		target ='warehouse' if not self.order_source else 'pur'
		if target == 'warehouse' :
			data = self.validate_warehouse()
		if target == 'pur':
			data = self.validate_purchase_order()
		self.total_warehouse_reseved()
		self.total_purchase_order_reseved()



	#?another query for validate purchase order

	# def add_row_single(self,target,data):		
	# 	if target=='warehouse':
	# 		self.warehouse = [] #?add row
	# 		row = self.append('warehouse', {})
	# 		row.bin = data.get("bin") 
	# 		row.warehouse = self.warehouse_source
	# 		row.reserved_qty = self.reservation_amount
	# 		# self.validate_warehouse()
	# 	if target== 'pur':
	# 		self.reservation_purchase_order = [] #?add row
	# 		row = self.append('reservation_purchase_order', {})
	# 		row.purchase_order_line = data.get("name")
	# 		row.purchase_order = self.order_source
	# 		row.qty = float(data.get("qty"))
	# 		row.reserved_qty = self.reservation_amount
	# 		# self.validate_purchase_order()
	# 	row.item = self.item_code
	# 	row.current_available_qty = float(data.get("qty"))
	# 	row.available_qty_atfer___reservation = data.get("qty") - self.reservation_amount