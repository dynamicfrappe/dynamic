# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters) , get_data(filters)
	return columns, data

def get_data(filters):
	quotation = filters.get("quotation")
	price_list = filters.get("price_list")

	doc = frappe.get_doc("Quotation" , quotation)
	items = doc.get("items")

	results = []
	for i in items:
		data = {}
		data['quotation'] = quotation
		data['item_code'] = i.item_code
		data['item_name'] = i.item_name
		data['qty'] = i.qty
		data['price_of_quotation'] = i.rate

		price = frappe.db.get_value("Item Price" , {"price_list" : price_list , "item_code" : i.item_code} , "price_list_rate")

		data['price_of_price_list'] = price
		data['total_of_quotation'] = float(i.qty or 0) * float(price or 0)
		data['diff'] = float(i.rate or 0) - float(price or 0)
		data['total_diff'] = float(i.qty or 0) * (float(i.rate or 0) - float(price or 0))
		data['per_diff'] = (float(i.rate or 0) - float(price or 0)) / float(price or 0) * 100


		results.append(data)
	return results

def get_columns(filters):
	columns = [
		{
			"fieldname": "quotation",
			"label": _("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation",
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
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"fieldname": "price_of_quotation",
			"label": _("Price of Quotation"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "price_of_price_list",
			"label": _("Price of Price List"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "total_of_quotation",
			"label": _("Total of Quotation"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "diff",
			"label": _("Difference"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "total_diff",
			"label": _("Total Difference"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "per_diff",
			"label": _("Percentage Difference"),
			"fieldtype": "Percentage",
			"width": 100,
		},
	]
	return columns
