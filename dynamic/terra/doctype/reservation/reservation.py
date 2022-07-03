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
			if not self.warehouse_source and not self.order_source:
				self.check_row()
				


	def check_row(self):
		if not self.warehouse_source and not self.order_source:
			if not len(self.warehouse) and not len(self.reservation_purchase_order):
				#1-check avail stock
				stock_sql = self.stock_pur_order_sql()
				# frappe.errprint(f'1--stock_sql-->{stock_sql}')
				# frappe.throw('thanks')
				# if stock_sql and len(stock_sql) > 0:#!commited
				# 	stock_sql +=frappe.db.sql("""select a.name,a.actual_qty ,'Bin' as doctype  FROM `tabBin` a where a.name NOT IN('{bin1}') and item_code='{item_code}'""".format(bin1=stock_sql[0].get('bin',"") if stock_sql else "",item_code=self.item_code),as_dict=1)
				#2-check avail purchase
				used_pur_order_name =  frappe.db.sql_list(f"""                   
										SELECT a.name as `name` ,a.parent,a.parenttype as doctype,
										CASE
										WHEN b.reserved_qty > 0 AND c.status="Active"
										then a.qty - SUM(b.reserved_qty)
										else a.qty
										end as qty
										from
										`tabPurchase Order Item` a
										LEFT JOIN
										`tabReservation Purchase Order` b
										ON b.purchase_order_line=a.name
										LEFT JOIN
										`tabReservation` c
										ON b.parent <> c.name
										
										where a.item_code = '{self.item_code}'
										""")
				res =  frappe.db.sql(f"""                   
										SELECT a.name as `name` ,a.parent,a.parenttype as doctype,
										CASE
											WHEN b.reserved_qty > 0 AND c.status="Active"
											then a.qty - SUM(b.reserved_qty)
											else a.qty
											end as qty
										from
										`tabPurchase Order Item` a
										LEFT JOIN
										`tabReservation Purchase Order` b
										ON b.purchase_order_line=a.name
										LEFT JOIN
										`tabReservation` c
										ON b.parent = c.name
										AND c.name <> "{self.name}"
										where a.item_code = '{self.item_code}'
										""",as_dict=1)
				
				# frappe.errprint(f'1--vstock_sql-->{stock_sql}')
				# frappe.throw('thanks')

				result_str_list = "" if not used_pur_order_name else ','.join([f"'{x}'" for x in used_pur_order_name])

				res += frappe.db.sql(f""" SELECT name,parent,parenttype as doctype , (qty - received_qty) as qty   FROM `tabPurchase Order Item` WHERE qty > 0 AND item_code = '{self.item_code}' AND name NOT IN({result_str_list}) """,as_dict=1)
				
				#3-check merge above
				sql_merge = stock_sql + res
				valid_bin_list = []
				valid_qty = 0
				
				frappe.errprint(f'sql_merge->{sql_merge}>')
				for row in sql_merge:
					frappe.errprint(f'lopp index>')
					flag = False
					if row.get('actual_qty')  and row.get('actual_qty') != None:
						valid_qty += row.get('actual_qty')
						valid_bin_list.append(row)
					elif row.get('qty')  and row.get('qty') != None :
						valid_qty += row.get('qty')
						valid_bin_list.append(row)					
					if(valid_qty >= self.reservation_amount):
						frappe.errprint(f'valid_qty check in if >')
						self.add_row_warehouse_test(valid_bin_list,self.reservation_amount)
						flag=True
						return
				
				else:
					if valid_qty < self.reservation_amount and flag==False:
						frappe.errprint(f'valid_qty throw err->{valid_qty}>')
						frappe.throw(f'Not available qty for Item {self.item_code}')
		
	
	def validate_warehouse(self):
		stock_sql = self.stock_sql()
		# frappe.errprint(f'stock_sql-->{stock_sql}')
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
	#validate Item in Purchase order 

	def stock_sql(self):
		return frappe.db.sql(f""" 
				      SELECT a.name as bin , 'Bin' as `doctype`,
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

	def stock_pur_order_sql(self):
		#todo: get list of used before
		test_name = frappe.db.sql_list(f"""
				select  a.name as bin, IF(b.reserved_qty>0, a.actual_qty-b.reserved_qty, a.actual_qty) as qty
				from tabBin  a, `tabReservation Warehouse` b, tabReservation c
				WHERE a.name = b.bin and a.item_code='{self.item_code}' and b.parent=c.name;
		""")
		frappe.errprint(f'test-->{test_name}')
		used_warehouse_name = frappe.db.sql_list("""
		 SELECT a.name as bin , 'Bin' as `doctype`,
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
                    ON b.parent = c.name AND c.name <> '{self.name}' AND a.item_code = '{self.item_code}'
					WHERE a.warehouse = b.warehouse
		""")
		result_str_list = f"''" if not test_name else ','.join([f"'{x}'" for x in test_name])
		frappe.errprint(f'result_str_list-->{result_str_list}')

		#Todo : get all before data
		test_all = frappe.db.sql(f"""
				select  a.name as bin,'Bin' as `doctype`, IF(b.reserved_qty>0, a.actual_qty-b.reserved_qty, a.actual_qty) as qty
				from tabBin  a, `tabReservation Warehouse` b, tabReservation c
				WHERE a.name = b.bin and a.item_code='{self.item_code}' and b.parent=c.name;
		""",as_dict=1)
		
		#Todo : get not used if found
		test_all += frappe.db.sql(f""" SELECT name as bin ,'Bin' as doctype , actual_qty as qty   FROM `tabBin` WHERE actual_qty > 0 AND item_code = '{self.item_code}' AND name NOT IN ({result_str_list}) ; """,as_dict=1)
		frappe.errprint(f'test2-->{test_all}')
		return test_all

	def validate_purchase_order(self):
		order = frappe.db.sql(f""" SELECT 
		  name , (qty - received_qty) as qty   FROM 
		 `tabPurchase Order Item` WHERE parent = '{self.order_source}' 
		 and item_code = '{self.item_code}' """,as_dict=1)
		
		# frappe.errprint(f'order qty from purchase order item-->{order}')
		if order and len(order) > 0 :
			if order[0].get("name") and float(order[0].get("qty")) > 0 :
				valid = self.validate_order_line(order[0].get("name") , float(order[0].get("qty")))
				if not valid :
					frappe.throw(_("Required Qty not Available In Purchase Order !"))
				if valid:
					self.reservation_purchase_order = [] #?add row
					row = self.append('reservation_purchase_order', {})
					row.item = self.item_code
					row.purchase_order_line = order[0].get("name")
					row.purchase_order = self.order_source
					row.qty = self.reservation_amount
					row.reserved_qty = self.reservation_amount
					row.current_available_qty = float(order[0].get("qty"))
					row.available_qty_atfer___reservation = float(order[0].get("qty")) - self.reservation_amount
			
			if order[0].get("name") and float(order[0].get("qty")) ==  0 :
				frappe.throw(_(f"  Purchase Order {self.order_source} dont have {self.item_code} avaliable Stock" ))
			if not order[0].get("name") :
				frappe.throw(_(f"  Purchase Order {self.order_source} dont have item {self.item_code}" ))	
		if not order or  len(order) == 0 :
			frappe.throw(_(f"Invalid Purchase Order {self.order_source} dont have item {self.item_code}"))
	
	def validate_order_line(self , line , qty ):
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
		




	def add_row_warehouse_test(self,valid_data,main_qty_row): # 2 1 3 6 -->10
		frappe.errprint(f'valid_data-->{valid_data}')
		# frappe.throw('thanks')

		main_qty_row_test = main_qty_row
		self.warehouse = []
		self.reservation_purchase_order = []
		for data in valid_data:
			frappe.errprint(f'data-->{data}')
			if data.get('doctype') == 'Bin':
				row = self.append('warehouse', {})
				row.item = self.item_name
				row_name = data.get('bin')
				row.bin = row_name
				frappe.errprint(f'row_name-->{row_name}')
				bin_doc = frappe.get_doc('Bin',row_name)
				row.warehouse = bin_doc.warehouse
				if main_qty_row_test >= data.qty:
					row.reserved_qty = data.qty
					row.current_available_qty = data.qty
					row.available_qty_atfer___reservation = 0
				else:
					row.reserved_qty = main_qty_row_test
					row.current_available_qty = data.qty #TODO  - main_qty_row_test
					row.available_qty_atfer___reservation = data.qty - main_qty_row_test #TODO edit it
				main_qty_row_test -= data.qty

				
			else:
				row = self.append('reservation_purchase_order', {})
				row.item = self.item_code
				row.purchase_order_line = data.get("name")
				row.purchase_order = data.parent
				row.qty = data.get('qty')
				if main_qty_row_test >= data.qty: #7-4-->6
					row.reserved_qty = data.qty#4
					row.current_available_qty = data.qty #4
					row.available_qty_atfer___reservation =  data.qty - main_qty_row_test if (data.qty - main_qty_row_test) > 0 else 0
				else:
					row.reserved_qty = main_qty_row_test
					row.current_available_qty = data.qty
					row.available_qty_atfer___reservation = data.qty - main_qty_row_test
				main_qty_row_test -= data.qty


			 # 
				
			# row = self.append('warehouse', {})
			# row.item = self.item_name
			# row.wharehouse = row.warehouse
			# if main_qty_row_test >= row.actual_qty:
			# 	# frappe.errprint(f'if-- main_qty_row_test--> {main_qty_row_test}')
			# 	row.reserved_qty = row.actual_qty
			# 	row.current_available_qty = 0
			# else:
			# 	# frappe.errprint(f'else-- main_qty_row_test--> {main_qty_row_test}')
			# 	row.reserved_qty = main_qty_row_test
			# 	row.current_available_qty = row.actual_qty - main_qty_row_test



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


# frappe.db.sql("""select a.name,a.actual_qty   FROM `tabBin` a where a.name NOT IN('{bin1}') and item_code='t1'""".format(bin1=d['bin']),as_dict=1)
#?------------

	# def bin_list_check(self,conditions,row):
	# 	bin_list = frappe.db.sql(
	# 	"""select item_code, warehouse, actual_qty,projected_qty
	# 	from tabBin bin {conditions} order by item_code, warehouse
	# 	""".format(
	# 		conditions= conditions if conditions else ""
	# 	),as_dict=1,)
	# 	if bin_list and self.warehouse_source:
	# 		for bin_dict in bin_list:
	# 			if bin_dict.projected_qty >= row.reserved_qty:
	# 				row.warehouse = bin_dict.warehouse
	# 				row.current_available_qty = bin_dict.projected_qty - row.reserved_qty
	# 				break

	# 	elif bin_list  and not self.warehouse_source and not self.order_source:
	# 		main_qty_row = row.reserved_qty
	# 		get_qty = False
	# 		for bin_dict in bin_list:
	# 			if bin_dict.projected_qty >= row.reserved_qty:
	# 				row.warehouse = bin_dict.warehouse
	# 				row.current_available_qty = bin_dict.projected_qty - main_qty_row
	# 				get_qty = True
	# 				break
	# 		else:
	# 			if  get_qty == False:
	# 				valid_bin_list = []
	# 				valid_qty = 0
	# 				for bin in bin_list:
	# 					valid_qty += bin.actual_qty
	# 					valid_bin_list.append(bin)
	# 					if(valid_qty >= main_qty_row):
	# 						self.add_row_warehouse_test(valid_bin_list,main_qty_row)
	# 						get_qty = True
	# 						break	
	# 				else:
	# 					if get_qty == False:
	# 						frappe.throw(f'Not available qty for Item {self.item_code}')
		# -----------------
		# frappe.errprint(f'test_all-->{test_all}')
		# res= frappe.db.sql(f""" 
		# 		      SELECT a.name as bin , 'Bin' as `doctype`,
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
        #             ON b.parent = c.name AND c.name <> "{self.name}" AND a.item_code = '{self.item_code}'
		# 			WHERE a.warehouse = b.warehouse
	
		# 			""" ,as_dict=1)