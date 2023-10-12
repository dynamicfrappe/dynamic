# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	return columns, data

def get_data(filters) :
	coditions= "so.docstatus = 1"

	if filters.get("sales_order"):
		coditions += f" AND so.name = '{filters.get('sales_order')}' "
	if filters.get("from_date") and filters.get("to_date"):
		coditions += f" AND so.transaction_date between '{filters.get('from_date')}' and '{filters.get('to_date')}'"
	
	sql = f""" SELECT so.name , i.item_code , i.qty , i.delivered_qty , (i.qty - i.delivered_qty) as undelivered_qty
	FROM `tabSales Order` so LEFT JOIN `tabSales Order Item` i ON 
	i.parent = so.name
	WHERE {coditions}"""
	data = frappe.db.sql(sql , as_dict = 1)
	return data

def get_columns():
	return [
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 180,
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 180,
		},
		{
			"label": _("Quantity"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"label": _("Delivered Quantity"),
			"fieldname": "delivered_qty",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"label": _("Undelivered Quantity"),
			"fieldname": "undelivered_qty",
			"fieldtype": "Float",
			"width": 180,
		},
	]