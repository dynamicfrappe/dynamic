# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from pickle import TRUE
import frappe
from frappe.model.document import Document

class Reservation(Document):
	def validate(self):
		if(not self.sales_order):
			self.check_available_ietm_in_stock()
	

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
