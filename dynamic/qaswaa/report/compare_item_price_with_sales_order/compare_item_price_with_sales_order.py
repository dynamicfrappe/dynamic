# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_date(filters)
	return columns, data

def get_date(filters):
	sales_order = filters.get("sales_order")
	price_list = filters.get("price_list")

	doc = frappe.get_doc("Sales Order" , sales_order)
	items = doc.get("items")

	results = []

	price_of_sales_order = 0
	total_of_sales_order = 0
	diff = 0

	for i in items:
		data = {}
		data['sales_order'] = sales_order
		data['item_code'] = i.item_code
		data['item_name'] = i.item_name
		data['qty'] = i.qty
		data['price_of_sales_order'] = i.rate

		price = frappe.db.get_value("Item Price" , {"price_list" : price_list , "item_code" : i.item_code} , "price_list_rate")

		data['price_of_price_list'] = price

		temp = float(i.qty or 0) * float(price or 0)
		data['total_of_sales_order'] = temp
		
		data['diff'] = float(i.rate or 0) - float(price or 0)
		data['total_diff'] = float(i.qty or 0) * (float(i.rate or 0) - float(price or 0))
		data['per_diff'] = (float(i.rate or 0) - float(price or 0)) / float(price or 0) * 100

		price_of_sales_order += data['price_of_sales_order']
		total_of_sales_order += temp
		diff += data['diff']

		results.append(data)
	results.append(())
	results.append(("","","","","Total rates of sales with sales order" , price_of_sales_order))
	results.append(("","","","","Total rates of sales with item price" , total_of_sales_order))
	results.append(("","","","","Total Differante" , diff))
	results.append(("","","","","Percentage of Sales Order" , float(diff) / float(total_of_sales_order) * 100))
	return results
	

def get_columns(filters):
	columns = [
		{
			"fieldname": "sales_order",
			"label": _("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 200,
		},
		{
			"fieldname": "item_code",
			"label": _("Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "qty",
			"label": _("Quantity"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "price_of_sales_order",
			"label": _("Price of Sales Order"),
			"fieldtype": "Data",
			"width": 250,
		},
		{
			"fieldname": "price_of_price_list",
			"label": _("Price of Price List"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "total_of_sales_order",
			"label": _("Total of Sales Order"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "diff",
			"label": _("Difference"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "total_diff",
			"label": _("Total Difference"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "per_diff",
			"label": _("Percentage Difference"),
			"fieldtype": "Data",
			"width": 100,
		},
	]
	return columns
