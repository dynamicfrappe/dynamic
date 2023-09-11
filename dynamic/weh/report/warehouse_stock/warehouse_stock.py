# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 



def execute(filters=None):
	return  WarehouseStock(filters).run()
class WarehouseStock(object):
	def __init__(self, filters=None):
		self.filters   = frappe._dict(filters or {})
		self.warehouses = []
		self.columns   = []
		self.data      = []
		self.map_data = []

	def set_warehouses(self , warehouses) :
		count =1
		data = []
		map_doc = {}
		
		for wh in warehouses :
			name = f"warehouse_{count}"
			obj = {
				"label": (f"{wh}"),
				"fieldtype": "data",
				"fieldname":  name,
				"width": 150
			} 
			data.append(obj)
			count = count +1 
			map_doc[name] = wh
		self.map_data  = map_doc 
		self.warehouses = data
		
	def run(self):
		
		if self.filters.get("warehouse") :
			self.set_warehouses( self.filters.get("warehouse") )
		self.columns = self.get_columns()
		self.data = self.get_data()
		return self.columns , self.data
	def get_columns(self, filters=None) :
		
		columns = [
			{
				"label": _("Item Code"),
				"fieldname": "item_code",
				"fieldtype": "Data",
				"width": 150
			},
			{
				"label": _("Item name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 250
			},
			{
				"label": _("Item Group"),
				"fieldname": "item_group",
				"fieldtype": "Data",
				"width": 150
			},
			{
				"label": _("Brand"),
				"fieldname": "brand",
				"fieldtype": "Data",
				"width": 150
			},
		]
		if self.warehouses :
			columns = columns + self.warehouses


		#add total row

		columns  = columns  + [{
				"label": _("Total"),
				"fieldname": "total",
				"fieldtype": "Data",
				"width": 150
			}]
		return columns
	def get_data(self) :
		data = []
		warehouse_str = ''
		cases = ""
		
		if self.warehouses :
			for k in self.warehouses  :
				warehouse_str = warehouse_str + f" '{k.get('label')}' ,"
				cases = cases + f""" 
				(select  SUM(actual_qty)  from `tabBin` where 
					warehouse =   '{k.get('label')}'  and item_code= a.item_code )  as '{k.get('fieldname')}' ,
				"""
			sql  = f"""  select a.item_code , b.item_name ,b.item_group , b.brand, sum(a.actual_qty) as total,
						
					 {cases[:-1]} 
					 ( 0 ) as total_2
					FROM `tabBin` a 
					inner join  `tabItem` b 
					ON b.name = a.item_code
					WHERE a.warehouse in ({warehouse_str[:-1]}) 

				
					"""
			

			"""
			select a.item_code , b.item_name ,b.item_group , b.brand, 
			(select  actual_qty  from `tabBin` where 
			warehouse =  "القوافل الطبية - WEH" and item_code= a.item_code)  as warehouse_1  ,
			(select  actual_qty  from `tabBin` where 
			warehouse =  "مخزن رئيسي - WEH" and item_code= a.item_code)  as warehouse_2 , 
			((select  actual_qty  from `tabBin` where 
			warehouse =  "القوافل الطبية - WEH" and item_code= a.item_code)  + (select  actual_qty  from `tabBin` where 
			warehouse =  "مخزن رئيسي - WEH" and item_code= a.item_code) ) as total
			FROM `tabBin` a inner join `tabItem` b ON b.name = a.item_code
			WHERE a.warehouse in ( 'القوافل الطبية - WEH' , 'مخزن رئيسي - WEH' ) 
			AND b.item_code = 'D0375' 
			GROUP By a.item_code ;
			
			
			"""
			if self.filters.get("item_code") :
				sql = sql + f"""AND b.item_code = '{self.filters.get("item_code")}' """

			if self.filters.get("item_group") :
				sql = sql + f"""AND b.item_group = '{self.filters.get("item_group")}' """

			if self.filters.get("brand") :
				sql = sql + f"""AND b.brand = '{self.filters.get("brand")}' """

			# if self.filters.get("from_date") :
			# 	sql = sql + f"""AND b.creation = '{self.filters.get("from_date")}' """
			
			# if self.filters.get("to_date") :
			# 	sql = sql + f"""AND b.creation = '{self.filters.get("to_date")}' """

			sql = sql +"	GROUP By  a.item_code "
			data = frappe.db.sql(sql ,as_dict=1)

			# frappe.throw(str(sql))
			return data
		return data

