# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters=None):
	conditions = " 1 = 1 "

	if filters.get("item_code") : 
		conditions += f" and item.item_code = '{filters.get('item_code')}' "
	if filters.get("item_name") : 
		conditions += f" and item.item_name = '{filters.get('item_name')}' "
	if filters.get("warehouse") : 
		conditions += f" and bin.warehouse = '{filters.get('warehouse')}' "

	sql= f'''
		select
			item.item_code,
			item.item_name,
			bin.warehouse,
			bin.actual_qty,
			item_reorder.warehouse_reorder_level,
			item_reorder.warehouse_reorder_qty
		From
			`tabItem` item
		Inner Join
			`tabBin` bin
		On
			item.name = bin.item_code
		Left Join 
			`tabItem Reorder` item_reorder
		On
			item.name = item_reorder.parent
		Where {conditions}

	'''

	data = frappe.db.sql(sql, as_dict = 1)
	return data




def get_columns(filters=None):
	columns = [
		#1
		{
			"fieldname" : "item_code",
			"label" : _("ID"),
			"fieldtype" : "Link",
			"options" : "Item",
			"width" : 300,
		},
		#2
		{
			"fieldname" : "item_name",
			"label" : _("Item Name"),
			"fieldtype" : "Link",
			"options" : "Item",
			"width" : 200,
		},
		#3
		{
			"fieldname" : "warehouse",
			"label" : _("Warehouse"),
			"fieldtype" : "Link",
			"options" : "warehouse",
			"width" : 200,
		},
		#4
		{
			"fieldname" : "actual_qty",
			"label" : _("Qty"),
			"fieldtype" : "Data",
			"width" : 100,
		},
		#5
		{
			"fieldname" : "warehouse_reorder_level",
			"label" : _("Re-order Level"),
			"fieldtype" : "Data",
			"width" : 150,
		},
		#6
		{
			"fieldname" : "warehouse_reorder_qty",
			"label" : _("Amount"),
			"fieldtype" : "Data",
			"width" : 100,
		},

	]
	return columns