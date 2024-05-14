# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters):
	condition = {}
	if filters.get("item_group"):
		condition["item_group"] = filters.get("item_group")
	if filters.get("brand"):
		condition["brand"] = filters.get("brand") 
	
	items = frappe.db.get_list("Item" , condition , ['item_code' , 'item_name' , 'item_group' , 'brand'])

	selling_price_list = filters.get('selling_price_list')
	buying_price_list = filters.get('buying_price_list')

	temp = []

	for item in items:
		selling = frappe.db.sql("""
		SELECT
			name,
			price_list_rate,
			price_list
		FROM
			`tabItem Price`
		WHERE
			item_code = %s
			AND selling = 1
			AND price_list = %s

		""",(item.item_code , selling_price_list) , as_dict= 1)

		buying = frappe.db.sql("""
		SELECT
			name,
			price_list_rate,
			price_list
		FROM
			`tabItem Price`
		WHERE
			item_code = %s
			AND buying = 1
			AND price_list = %s

		""", (item.item_code , buying_price_list) , as_dict= 1)

		if selling and buying:
			data = {}
			data["item_code"] = item.item_code
			data['item_name'] = item.item_name
			data['item_group'] = item.item_group
			data['brand'] = item.brand
			data["selling_price_list"] = selling[0]['price_list']
			data['price_of_selling'] = float(selling[0]['price_list_rate']) 
			data["buying_price_list"] = buying[0]['price_list']
			data['price_of_buying'] = float(buying[0]['price_list_rate'] )

			data['diff'] = data['price_of_selling'] - data['price_of_buying']
			if data['price_of_buying'] != 0:
				data['percentage'] = (data['price_of_selling'] / data['price_of_buying']) * 100
			else:
				data['percentage'] = 0 
			temp.append(data)
	return temp

def get_columns(filters):
	columns = [
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
			"fieldname": "selling_price_list",
			"label": _("Selling Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 200,
		},
		{
			"fieldname": "buying_price_list",
			"label": _("Buying Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 200,
		},
		{
			"fieldname": "item_group",
			"label": _("Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 200,
		},
		{
			"fieldname": "brand",
			"label": _("Brand"),
			"fieldtype": "Link",
			"options": "brand",
			"width": 100,
		},
		{
			"fieldname": "price_of_selling",
			"label": _("Price of selling"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "price_of_buying",
			"label": _("Price of buying"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "diff",
			"label": _("differante"),
			"fieldtype": "Currency",
			"width": 100,
		},
		{
			"fieldname": "percentage",
			"label": _("percentage"),
			"fieldtype": "Percentage",
			"width": 100,
		},
		
	]
	return columns
