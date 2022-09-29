# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from pickle import TRUE
import re
import frappe
from frappe.model.document import Document
from frappe import _ 
class Reservation(Document):

	def before_insert(self):
		#validate item 
		if not self.item_code :
			frappe .throw(_("Please Select Item First !"))
		# validate required qty 
		if float(self.reservation_amount or 0) == 0 or  float(self.reservation_amount or 0) < 0 :
			frappe.throw(_("Invalid Amount Required "))
		#validate source 
		if  self.warehouse_source and self.order_source :
			frappe.throw(_("Invalid Source "))
		#validate status 
		if self.status == "Active" :
			#validate warehouse case
			if self.warehouse_source :
				self.validate_warehouse()
			if self.order_source :
				self.validate_purchase_order()
			if not self.warehouse_source and not self.order_source:
				frappe.throw(_("Please Select Source As Warehouse Or Purchase Order for Item"))
				# self.get_pur_order_or_warehouse()

		if self.warehouse:
			self.total_warehouse_reseved()
		if self.reservation_purchase_order:
			self.total_purchase_order_reseved()
		
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
		if  not stock_sql and len(stock_sql) == 0 :
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
		# data2= f"""
		# 	select tb.name ,tb.item_code  ,tb.actual_qty  ,tb.reserved_qty,  (tb.actual_qty  -  sum(trw.reserved_qty)) as diff  from `tabReservation Warehouse` trw 
		# 	INNER JOIN tabBin tb 
		# 	ON tb.name  = trw.bin  
		# 	INNER JOIN tabReservation tr 
		# 	ON tr.name <> "{self.name}" AND trw.parent = tr.name AND tb.item_code = '{self.item_code}'
		# 	AND tb.warehouse = '{self.warehouse_source}' AND tb.item_code = '{self.item_code}'
		# """
		# data2 = frappe.db.sql(data2)
		# frappe.errprint(f'data is -> {data2}')
		# frappe.throw('wait')
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
	
		


	def add_row_single(self,target,data):		
		if target=='warehouse':
			self.warehouse = [] #?add row
			row = self.append('warehouse', {})
			row.bin = data.get("bin") 
			row.warehouse = self.warehouse_source
			row.reserved_qty = self.reservation_amount
		if target== 'pur':
			self.reservation_purchase_order = [] #?add row
			row = self.append('reservation_purchase_order', {})
			row.purchase_order_line = data.get("name")
			row.purchase_order = self.order_source
			row.qty = float(data.get("qty"))
			row.reserved_qty = self.reservation_amount
		row.item = self.item_code
		row.current_available_qty = float(data.get("qty"))
		row.available_qty_atfer___reservation = data.get("qty") - self.reservation_amount
		
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


	#?another query for validate purchase order
	# def validate_purchase_order_two(self):
	# 	order =  frappe.db.sql(f"""
	# 		SELECT a.name ,a.parent,a.parenttype as doctype , 
	# 		CASE
	# 		WHEN b.reserved_qty > 0 AND c.status <> "Invalid"
	# 		then (a.qty - a.received_qty) - SUM(b.reserved_qty)
	# 		else a.qty - a.received_qty
	# 		end as qty 
	# 		from `tabPurchase Order Item` a, `tabReservation Purchase Order` b,`tabReservation` c
	# 		WHERE a.item_code = '{self.item_code}' AND   b.purchase_order_line=a.name AND b.parent = c.name AND c.name <> '{self.name}' 
	# 		AND a.item_code = '{self.item_code}'  and a.parent = '{self.order_source}' 
	# 		GROUP  BY a.name
	# 	 """,as_dict=1)
	# 	return order
		

	#? used in validate_purchase_order
	# def validate_order_line(self , line , qty ):
	# 	res_sql = frappe.db.sql(""" SELECT SUM(reserved_qty) AS qty FROM `tabReservation Purchase Order`
	# 	WHERE item = '{self.item_code}' and purchase_order_line = '{line}'  """,as_dict = True)
	# 	if res_sql and len(res_sql) > 0 :
	# 		if qty  - float(res_sql[0].get('qty') or 0 ) >= self.reservation_amount :
	# 			return True
	# 		if qty  - float(res_sql[0].get('qty') or 0 ) < self.reservation_amount :
	# 			return False
	# 	else :
	# 		return True	

	# def validate_pur_order_unkown(self):
	# 	used_pur_order_name =  frappe.db.sql_list(f"""                   
	# 									SELECT a.name as `name` ,a.parent,a.parenttype as doctype,
	# 									CASE
	# 									WHEN b.reserved_qty > 0 AND c.status="Active"
	# 									then a.qty - SUM(b.reserved_qty)
	# 									else a.qty
	# 									end as qty
	# 									from
	# 									`tabPurchase Order Item` a
	# 									LEFT JOIN
	# 									`tabReservation Purchase Order` b
	# 									ON b.purchase_order_line=a.name
	# 									LEFT JOIN
	# 									`tabReservation` c
	# 									ON b.parent = c.name 
	# 									AND c.name <> '{self.name}'
	# 									where a.item_code = '{self.item_code}' and a.parent = '{self.order_source}'
	# 									""")
										
	# 	res =  frappe.db.sql(f"""                   
	# 									SELECT a.name as `name` ,a.parent,a.parenttype as doctype,
	# 									CASE
	# 										WHEN b.reserved_qty > 0 AND c.status="Active"
	# 										then a.qty - SUM(b.reserved_qty)
	# 										else a.qty
	# 										end as qty
	# 									from
	# 									`tabPurchase Order Item` a
	# 									LEFT JOIN
	# 									`tabReservation Purchase Order` b
	# 									ON b.purchase_order_line=a.name
	# 									LEFT JOIN
	# 									`tabReservation` c
	# 									ON b.parent = c.name
	# 									AND c.name <> "{self.name}"
	# 									where a.item_code = '{self.item_code}' and a.parent = '{self.order_source}'
	# 									""",as_dict=1)
		
	# 	result_str_list = "" if not used_pur_order_name else ','.join([f"'{x}'" for x in used_pur_order_name])
	# 	res += frappe.db.sql(f""" SELECT name,parent,parenttype as doctype , (qty - received_qty) as qty   FROM `tabPurchase Order Item` WHERE qty > 0 AND item_code = '{self.item_code}' AND name NOT IN({result_str_list}) """,as_dict=1)
	# 	return res

# def validate_stock_unkown(self):
	# 	#** get list of used before
	# 	used_warehouse = frappe.db.sql_list(f"""
	# 			select  a.name as bin, IF(b.reserved_qty>0, a.actual_qty-b.reserved_qty, a.actual_qty) as qty
	# 			from tabBin  a, `tabReservation Warehouse` b, tabReservation c
	# 			WHERE a.name = b.bin and a.item_code='{self.item_code}' and b.parent=c.name;
	# 	""")
		# used_warehouse_name = frappe.db.sql_list("""
		#  SELECT a.name as bin , 'Bin' as `doctype`,
		# 			CASE 
        #                  WHEN b.reserved_qty > 0 AND c.status="Active"
		# 				 then a.actual_qty - SUM(b.reserved_qty)
		# 				 ELSE a.actual_qty 
		# 				 END  as qty
		# 			 FROM 
		# 			`tabBin` a
		# 			LEFT JOIN 
		# 		   `tabReservation Warehouse` b 
		# 			ON a.name = b.bin 
        #              LEFT JOIN 
        #             `tabReservation` c
        #             ON b.parent = c.name AND c.name <> '{self.name}' AND a.item_code = '{self.item_code}'
		# 			WHERE a.warehouse = b.warehouse
		# """)
		# result_str_list = f"''" if not used_warehouse else ','.join([f"'{x}'" for x in used_warehouse])

		# #**: get all before data(used + un_used)
		# get_all_warehouse = frappe.db.sql(f"""
		# 		select  a.name as bin,'Bin' as `doctype`, IF(b.reserved_qty>0, a.actual_qty-b.reserved_qty, a.actual_qty) as qty
		# 		from tabBin  a, `tabReservation Warehouse` b, tabReservation c
		# 		WHERE a.name = b.bin and a.item_code='{self.item_code}' and b.parent=c.name;
		# """,as_dict=1)
		
		#** get not used if found
		# get_all_warehouse += frappe.db.sql(f""" SELECT name as bin ,'Bin' as doctype , actual_qty as qty   FROM `tabBin` WHERE actual_qty > 0 AND item_code = '{self.item_code}' AND name NOT IN ({result_str_list}) ; """,as_dict=1)
		# return get_all_warehouse
	# def add_row_warehouse_or_pur_order(self,valid_data,main_qty_row): # 2 1 3 6 -->10
	# 	main_qty_row_test = main_qty_row
	# 	self.warehouse = []
	# 	self.reservation_purchase_order = []
	# 	for data in valid_data:
	# 		if data.get('doctype') == 'Bin':
	# 			row = self.append('warehouse', {})
	# 			row.item = self.item_name
	# 			row_name = data.get('bin')
	# 			row.bin = row_name
	# 			bin_doc = frappe.get_doc('Bin',row_name)
	# 			row.warehouse = bin_doc.warehouse
	# 			if main_qty_row_test >= data.qty:
	# 				row.reserved_qty = data.qty
	# 				row.current_available_qty = data.qty
	# 				row.available_qty_atfer___reservation = 0
	# 			else:
	# 				row.reserved_qty = main_qty_row_test
	# 				row.current_available_qty = data.qty #TODO  - main_qty_row_test
	# 				row.available_qty_atfer___reservation = data.qty - main_qty_row_test #TODO edit it
	# 			main_qty_row_test -= data.qty

				
	# 		else:
	# 			row = self.append('reservation_purchase_order', {})
	# 			row.item = self.item_code
	# 			row.purchase_order_line = data.get("name")
	# 			row.purchase_order = data.parent
	# 			row.qty = data.get('qty')
	# 			if main_qty_row_test >= data.qty: #7-4-->6
	# 				row.reserved_qty = data.qty#4
	# 				row.current_available_qty = data.qty #4
	# 				row.available_qty_atfer___reservation =  data.qty - main_qty_row_test if (data.qty - main_qty_row_test) > 0 else 0
	# 			else:
	# 				row.reserved_qty = main_qty_row_test
	# 				row.current_available_qty = data.qty
	# 				row.available_qty_atfer___reservation = data.qty - main_qty_row_test
	# 			main_qty_row_test -= data.qty



	# def get_pur_order_or_warehouse(self):
	# 	if not self.warehouse_source and not self.order_source:
	# 		# if not len(self.warehouse) and not len(self.reservation_purchase_order):
	# 		#1-check avail stock
	# 		stock_sql = self.validate_stock_unkown()
	# 		res = self.validate_pur_order_unkown()
	# 		#3-check merge above
	# 		sql_merge = stock_sql + res
	# 		valid_bin_list = []
	# 		valid_qty = 0
			
	# 		for row in sql_merge:
	# 			flag = False
	# 			if row.get('actual_qty')  and row.get('actual_qty') != None:
	# 				valid_qty += row.get('actual_qty')
	# 				valid_bin_list.append(row)
	# 			elif row.get('qty')  and row.get('qty') != None :
	# 				valid_qty += row.get('qty')
	# 				valid_bin_list.append(row)					
	# 			if(valid_qty >= self.reservation_amount):
	# 				self.add_row_warehouse_or_pur_order(valid_bin_list,self.reservation_amount)
	# 				flag=True
	# 				return
			
	# 		else:
	# 			if valid_qty < self.reservation_amount and flag==False:
	# 				frappe.throw(f'Not available qty for Item {self.item_code}')
		
	