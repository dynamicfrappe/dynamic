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
	if filters.get("from_date"):
		conditions += " AND `tabStock Entry`.posting_date >= '%s' "%(filters.get("from_date"))
	if filters.get("to_date"):
		conditions += " AND `tabStock Entry`.posting_date <= '%s' "%(filters.get("to_date"))
	if filters.get("s_warehouse"):
		conditions += " AND `tabStock Entry Detail`.s_warehouse='%s' "%(filters.get("s_warehouse"))
	if filters.get("item_code"):
		conditions += " AND `tabStock Entry Detail`.item_code = '%s' "%(filters.get("item_code"))

	sql = f"""
	SELECT `tabStock Entry`.name
	,`tabStock Entry`.posting_date
	,`tabStock Entry Detail`.s_warehouse as from_warehouse
	,`tabStock Entry Detail`.t_warehouse as to_warehouse
	,`tabStock Entry Detail`.item_code
	,`tabStock Entry Detail`.item_name
	,`tabStock Entry Detail`.qty
	,`tabStock Entry Detail`.basic_rate
	,`tabStock Entry Detail`.amount
	FROM `tabStock Entry`
	INNER JOIN `tabStock Entry Detail`
	ON `tabStock Entry`.name=`tabStock Entry Detail`.parent
	WHERE `tabStock Entry`.stock_entry_type='Material Transfer' AND `tabStock Entry`.docstatus<>2 AND {conditions}
	"""
	
	# print('\n\n\n=***==sql>',sql,'\n\n\n')
	result = frappe.db.sql(sql,as_dict=1)
	# print('\n\n\n===result>',result,'\n\n\n')
	return result

def get_columns(filters):
	columns = [
		{
			"label": _("Name"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Stock Entry",
			"width": 150
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"label": _("From Warehouse"),
			"fieldname": "from_warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 150
		},
		{
			"label": _("To Warehouse"),
			"fieldname": "to_warehouse",
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
			"label": _("QTy"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Price"),
			"fieldname": "basic_rate",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Total Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 150
		},
		
		
		
	]
	
	return columns