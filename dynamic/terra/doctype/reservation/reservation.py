# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Reservation(Document):
	def validate(self):
        #1-check item in stock
		self.check_available_ietm_in_stock()
		#2-check item in purchase order
		


	
	def check_available_ietm_in_stock(self):
		warehouse_data = self.warehouse
		for row in warehouse_data:
			##? for each item in reservation check its projected_qty(available) by warehouse
			self.get_avail_qty_for_item(row)
			#** check which avail qty is suitable for reservation qty
			
			
	def get_avail_qty_for_item(self,row):
		# frappe.errprint(f'get_avail_qty_for_item-->')
		if not self.warehouse_source:
			conditions =f" where item_code='{self.item_code}'"
		else:
			# frappe.errprint(f'else warehouse-->{self.warehouse_source}')
			conditions =f" where item_code='{self.item_code}' and warehouse = '{self.warehouse_source}'"
		
		bin_list = frappe.db.sql(
		"""select item_code, warehouse, actual_qty,projected_qty
		from tabBin bin {conditions} order by item_code, warehouse
		""".format(
			conditions= conditions if conditions else ""
		),
		as_dict=1,
		)
		# frappe.throw(f'thanks')
		if bin_list and self.warehouse_source:
			for bin_dict in bin_list:
				if bin_dict.projected_qty >= row.reserved_qty:
					row.warehouse = bin_dict.warehouse

		elif bin_list  and not self.warehouse_source:
			#get multi warehouse
			main_qty_row = row.reserved_qty
			index = 0
			frappe.errprint(f'bin_list ---> {bin_list}')
			for bin_dict in bin_list:
				index +=1
				if bin_dict.projected_qty >= row.reserved_qty:
					row.warehouse = bin_dict.warehouse
				elif bin_dict.projected_qty < row.reserved_qty:#for to check found avail warehouse has qty
					for index_first in range(len(bin_list)):
						for index_sec in range(index_first+1,len(bin_list)):
							if bin_list[index_first].projected_qty + bin_list[index_sec].projected_qty >= row.reserved_qty: # 5 + 4 --> 6
								frappe.errprint(f'selected ---> {bin_list[index_first].projected_qty}--{bin_list[index_sec].projected_qty}')
								self.append('warehouse', {
								'item': self.item_name,
								'reserved_qty': bin_list[index_first].projected_qty,#5
								'wharehouse': bin_list[index_first].warehouse,
								'current_available_qty':0
								})
								change_qty = main_qty_row - bin_list[index_first].projected_qty
								self.append('warehouse', {
								'item': self.item_name,
								'reserved_qty': main_qty_row - bin_list[index_first].projected_qty ,
								'wharehouse': bin_list[index_sec].warehouse,
								'current_available_qty':bin_list[index_sec].projected_qty - change_qty
								})
								del self.warehouse[index-1]
								# frappe.errprint(f'reserved warehouse items-22222->{self.warehouse}---{type(self.warehouse)}')
								# frappe.errprint('test')
								# frappe.throw(f'thanks')
								break
						break
				else:
					frappe.throw(f'Not available qty for Item {self.item_code}')
				break
		else:
			frappe.throw(f'Not available qty for Item {self.item_code}')

