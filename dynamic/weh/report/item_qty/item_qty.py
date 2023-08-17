# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_data(filters):
	conditions = " 1=1 "
	if filters.get("warehouse"):
		warehouse_list = ','.join([f"'{x}'" for x in filters.get("warehouse")]) 
		# print('\n\n\n===warehouse_list>',warehouse_list,'\n\n\n')
		conditions += f" AND `tabBin`.warehouse IN ({warehouse_list}) "
	if filters.get("item_code"):
		conditions += " AND `tabBin`.item_code = '%s' "%(filters.get("item_code"))

	sql = f"""
	select `tabBin`.actual_qty
	,(`tabBin`.actual_qty-`tabBin`.reserved_qty)actual_after_reserved
	,`tabBin`.warehouse,`tabBin`.item_code  from `tabBin`
	WHERE {conditions} 
	"""

	# d =  [
	# 'D0054': {'actual_qty': 19.0, 'actual_after_reserved': 19.0, 'warehouse': 'مخزن رئيسي - WEH', 'item_code': 'D0054', 'مخزن رئيسي - WEH': 19.0, 'المعمل - WEH': 10.0},
	# ]
	# print('\n\n\n=***==sql>',sql,'\n\n\n')
	result = frappe.db.sql(sql,as_dict=1)
	data = frappe._dict()
	last_data=[]
	#** ex : {'D0375': {'actual_qty': 10.0, 'actual_after_reserved': 10.0, 'warehouse': 'مخزن رئيسي - WEH', 'item_code': 'D0375', 'مخزن رئيسي - WEH': 'مخزن رئيسي - WEH'},
	for row in result:
		if row.item_code not in data:
			data[row.item_code] = row
			data[row.item_code][row.warehouse] = row.actual_qty
		if row.item_code in data:
			data[row.item_code][row.warehouse] = row.actual_qty

	for k,v in data.items():
		last_data.append(v)
		
	print('\n\n\n===last_data>',last_data,'\n\n\n')
	return last_data

def get_columns(filters):
	columns = [
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Actual QTY"),
			"fieldname": "actual_qty",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Actual QTY After Reserved"),
			"fieldname": "actual_after_reserved",
			"fieldtype": "Float",
			"width": 150
		},
		# {
		# 	"label": _("Warehouse"),
		# 	"fieldname": "warehouse",
		# 	"fieldtype": "Data",
		# 	"width": 150
		# },
		
	]
	if filters.get("warehouse"):
		for warehouse in filters.get("warehouse"):
			columns.extend([
				{
					"label":_("{0}").format(warehouse),
					"fieldname": _("{0}").format(warehouse),
					"fieldtype": "Data",
					"width": 150
				},
				])
	# 	warehouse_list = ','.join(filters.get("warehouse"))
	return columns