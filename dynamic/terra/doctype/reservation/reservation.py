# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from pickle import TRUE
import re
import frappe
from frappe.model.document import Document
from frappe import _ 
class Reservation(Document):
	def validate(self):

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
			pass



		# if(not self.sales_order):
		# 	self.check_available_ietm_in_stock()
	# Check if reservation_amount is valid and is available in ware house 
	def validate_warehouse(self):
		stock_sql = frappe.db.sql(f""" 
				      SELECT a.name as bin , 
					CASE 
                         WHEN b.reserved_qty > 0 AND c.status="Active"
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
		if stock_sql and len(stock_sql) > 0 :

			if stock_sql[0].get("qty") == 0 or float( stock_sql[0].get("qty")  or 0 ) < self.reservation_amount  :
				frappe.throw(_(f""" stock value in warehouse {self.warehouse_source} = {stock_sql[0].get("qty")} 
				  and you requires  {self.reservation_amount}  """))

			self.warehouse = []
			row = self.append('warehouse', {})
			row.item = self.item_code
			row.bin = stock_sql[0].get("bin") 
			row.warehouse = self.warehouse_source
			row.current_available_qty = stock_sql[0].get("qty") 
			row.reserved_qty = self.reservation_amount
			row.available_qty_atfer___reservation = stock_sql[0].get("qty") - self.reservation_amount
		if  not stock_sql and len(stock_sql) == 0 :
			frappe.throw(_(f""" no stock value in warehouse {self.warehouse_source} for item {self.item_code}  """))
	#validate Item in Purchase order 
	def validate_purchase_order(self):
		order = frappe.db.sql(f""" SELECT 
		  name , (qty - received_qty) as qty   FROM 
		 `tabPurchase Order Item` WHERE parent = '{self.order_source}' 
		 and item_code = '{self.item_code}' """,as_dict=1)
		
		# frappe.errprint(f'order -->{order}')
		if order and len(order) > 0 :
			if order[0].get("name") and float(order[0].get("qty")) > 0 :
				valid = self.validate_order_line(order[0].get("name") , float(order[0].get("qty")))
				if not valid :
					frappe.throw(_("Required Qty not Available In Purchase Order !"))
				
			
			if order[0].get("name") and float(order[0].get("qty")) ==  0 :
				frappe.throw(_(f"  Purchase Order {self.order_source} dont have {self.item_code} avaliable Stock" ))
			if not order[0].get("name") :
				frappe.throw(_(f"  Purchase Order {self.order_source} dont have item {self.item_code}" ))	
		if not order or  len(order) == 0 :
			frappe.throw(_(f"Invalid Purchase Order {self.order_source} dont have item {self.item_code}"))
	
	def validate_order_line(self , line , qty ):
		#check reseved qty from order line 
		res_sql = frappe.db.sql(""" SELECT SUM(reserved_qty) AS qty FROM `tabReservation Purchase Order`
		WHERE item = '{self.item_code}' and purchase_order_line = '{line}'  """,as_dict = True)
		if res_sql and len(res_sql) > 0 :
			if qty  - float(res_sql[0].get('qty') or 0 ) > self.reservation_amount :
				return True
			if qty  - float(res_sql[0].get('qty') or 0 ) < self.reservation_amount :
				return False
		else :
			return True
	def check_available_ietm_in_stock(self):
		if not self.order_source:
			warehouse_data = self.warehouse
			self.get_avail_qty_for_item_warehouse(self.warehouse[0])
			# for row in warehouse_data:
			# 	self.get_avail_qty_for_item_warehouse(row)
		else:
			purchase_order_items = self.reservation_purchase_order
			# for index in len(purchase_order_items):
				# self.get_avail_qty_for_item_purchase_order(purchase_order_items[0])
			for p_row in purchase_order_items:
				self.get_avail_qty_for_item_purchase_order(p_row)
			
			
	def get_avail_qty_for_item_warehouse(self,row):
		if not self.warehouse_source:
			conditions =f" where item_code='{self.item_code}'"
			self.bin_list_check(conditions,row)
		elif not self.warehouse_source and not self.purchase_order:
			conditions =f" where item_code='{self.item_code}' and warehouse = '{self.warehouse_source}'"
			self.bin_list_check(conditions,row)
			

	def get_avail_qty_for_item_purchase_order(self,row):
		self.get_purchase_order_qty(row)

		
	def get_purchase_order_qty(self,row):
		purchase_prder_list = frappe.db.sql("""select SUM(qty) as total_reserved_qty from `tabReservation  Purchase Order` where `tabReservation  Purchase Order`.`purchase_order` ='{purchase_order}'  and parent IN (select name from tabReservation tr where status = 'Active')""".format(purchase_order=self.order_source),as_dict=1,
		)
		total_reserved_qty = purchase_prder_list[0]['total_reserved_qty'] if purchase_prder_list[0]['total_reserved_qty'] else 0
		actual_qty_list = frappe.db.sql("""
			select parent,qty,item_code from `tabPurchase Order Item` tpoi where parent='{purchase_order}' and item_code='{item_code}'
		""".format(purchase_order=self.order_source,item_code=self.item_code),as_dict=1)
		actual_qty = actual_qty_list[0]['qty']
		avail_qty = actual_qty - total_reserved_qty
		
		if row.qty > avail_qty:
			frappe.throw(f'Not available qty for Item {self.item_code} in purchase order {self.order_source}')
		else:
			row.current_available_qty = avail_qty
			row.purchase_order_line = self.item_code
			row.available_qty_atfer___reservation = avail_qty - row.qty
			row.reserved_qty = total_reserved_qty
		


	def bin_list_check(self,conditions,row):
		bin_list = frappe.db.sql(
		"""select item_code, warehouse, actual_qty,projected_qty
		from tabBin bin {conditions} order by item_code, warehouse
		""".format(
			conditions= conditions if conditions else ""
		),as_dict=1,)
		if bin_list and self.warehouse_source:
			for bin_dict in bin_list:
				if bin_dict.projected_qty >= row.reserved_qty:
					row.warehouse = bin_dict.warehouse
					row.current_available_qty = bin_dict.projected_qty - row.reserved_qty
					break

		elif bin_list  and not self.warehouse_source and not self.order_source:
			main_qty_row = row.reserved_qty
			get_qty = False
			for bin_dict in bin_list:
				if bin_dict.projected_qty >= row.reserved_qty:
					row.warehouse = bin_dict.warehouse
					row.current_available_qty = bin_dict.projected_qty - main_qty_row
					get_qty = True
					break
			else:
				if  get_qty == False:
					valid_bin_list = []
					valid_qty = 0
					for bin in bin_list:
						valid_qty += bin.actual_qty
						valid_bin_list.append(bin)
						if(valid_qty >= main_qty_row):
							self.add_row_warehouse_test(valid_bin_list,main_qty_row)
							get_qty = True
							break	
					else:
						if get_qty == False:
							frappe.throw(f'Not available qty for Item {self.item_code}')
		


	def add_row_warehouse_test(self,valid_bin_list,main_qty_row): # 2 1 3 6 -->10
		main_qty_row_test = main_qty_row
		del self.warehouse[0]
		# frappe.errprint(f'valid bins--> {valid_bin_list}')
		for bin in valid_bin_list:
			row = self.append('warehouse', {})
			row.item = self.item_name
			row.wharehouse = bin.warehouse
			if main_qty_row_test >= bin.actual_qty:
				# frappe.errprint(f'if-- main_qty_row_test--> {main_qty_row_test}')
				row.reserved_qty = bin.actual_qty
				row.current_available_qty = 0
			else:
				# frappe.errprint(f'else-- main_qty_row_test--> {main_qty_row_test}')
				row.reserved_qty = main_qty_row_test
				row.current_available_qty = bin.actual_qty - main_qty_row_test
			main_qty_row_test -= bin.actual_qty # 



#? -----------
# bin_list = frappe.db.sql(
		# """select item_code, warehouse, actual_qty,projected_qty
		# from tabBin bin {conditions} order by item_code, warehouse
		# """.format(
		# 	conditions= conditions if conditions else ""
		# ),
		# as_dict=1,
		# )
		# if bin_list and self.warehouse_source:
		# 	for bin_dict in bin_list:
		# 		if bin_dict.projected_qty >= row.reserved_qty:
		# 			row.warehouse = bin_dict.warehouse
		# 			row.current_available_qty = bin_dict.projected_qty - row.reserved_qty
		# 			break

		# elif bin_list  and not self.warehouse_source and not self.order_source:
			# main_qty_row = row.reserved_qty
			# get_qty = False
			# for bin_dict in bin_list:
			# 	if bin_dict.projected_qty >= row.reserved_qty:
			# 		row.warehouse = bin_dict.warehouse
			# 		row.current_available_qty = bin_dict.projected_qty - main_qty_row
			# 		get_qty = True
			# 		break
			# else:
			# 	if  get_qty == False:
			# 		for index_first in range(len(bin_list)-1):
			# 			for index_sec in range(index_first+1,len(bin_list)):
							
			# 				if bin_list[index_first].projected_qty + bin_list[index_sec].projected_qty >= row.reserved_qty: # 5 + 4 --> 6
			# 					self.add_row_warehouse(bin_list[index_first],bin_list[index_sec],main_qty_row)
			# 					get_qty = True
								
			# 		else:
			# 			if get_qty == False:
			# 				frappe.throw(f'Not available qty for Item {self.item_code}')
			# 	else:
			# 		frappe.throw(f'Not available qty for Item {self.item_code}')


			#?-----end--------

				# def add_row_warehouse(self,bin1,bin2,main_qty_row): #stores D =4 ,, Goods In Transit - D=5
	# 	frappe.errprint(f'bin1 --> {bin1}')
	# 	frappe.errprint(f'bin2 --> {bin2}')

	# 	row = self.append('warehouse', {})
	# 	row.item = self.item_name
	# 	row.reserved_qty = bin1.projected_qty
	# 	row.wharehouse = bin1.warehouse
	# 	row.current_available_qty = 0

	# 	change_qty = main_qty_row - bin1.projected_qty
	# 	row2 = self.append('warehouse', {})
	# 	row2.item = self.item_name
	# 	row2.reserved_qty = change_qty
	# 	row2.wharehouse = bin2.warehouse
	# 	row2.current_available_qty = bin2.projected_qty - change_qty
	# 	del self.warehouse[0]
