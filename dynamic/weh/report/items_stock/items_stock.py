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
		# print('\n\n\n===warehouse_list>',warehouse_list,'\n\n\n')
		conditions += " AND `tabBin`.warehouse='%s' "%(filters.get("warehouse"))
	if filters.get("item_code"):
		conditions += " AND `tabBin`.item_code = '%s' "%(filters.get("item_code"))

	
	if filters.get("item_group"):
		conditions += " AND `tabItem`.item_group = '%s' "%(filters.get("item_group"))

	if filters.get("parent_group"):
		conditions += " AND `tabItem`.parent_group = '%s' "%(filters.get("parent_group"))

	if filters.get("brand"):
		conditions += " AND `tabItem`.brand = '%s' "%(filters.get("brand"))

	sql = f"""
	select `tabBin`.actual_qty
	,(`tabBin`.actual_qty-`tabBin`.reserved_qty)actual_after_reserved
	,`tabBin`.warehouse,`tabBin`.item_code
	,`tabItem`.item_group,`tabItem`.brand , `tabItem`.item_name ,`tabItem`.parent_group 
	FROM `tabBin`
	INNER JOIN `tabItem`
	ON `tabItem`.item_code=`tabBin`.item_code
	WHERE {conditions}
	"""
	
	# print('\n\n\n=***==sql>',sql,'\n\n\n')
	result = frappe.db.sql(sql,as_dict=1)
	# print('\n\n\n===result>',result,'\n\n\n')
	return result

def get_columns(filters):
	columns = [
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Brand"),
			"fieldname": "brand",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Parent Group"),
			"fieldname": "parent_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 150
		},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 150
		},
		{
			"label": _("Actual QTY"),
			"fieldname": "actual_qty",
			"fieldtype": "Float",
			"width": 150
		},
		# {
		# 	"label": _("Actual QTY After Reserved"),
		# 	"fieldname": "actual_after_reserved",
		# 	"fieldtype": "Float",
		# 	"width": 150
		# },
		
		
	]
	
	return columns