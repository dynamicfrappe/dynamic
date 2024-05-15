# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_last_purchase_invoice_for_item , get_last_sales_invoice_for_item



def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters):
	sales_invoice = filters.get("sales_invoice")

	doc = frappe.get_doc("Sales Invoice" , sales_invoice)
	items = doc.get("items")

	results = []

	total1 = 0
	total2 = 0

	for i in items:
		data = {}
		data['sales_invoice'] = sales_invoice
		data['item_code'] = i.item_code
		data['item_name'] = i.item_name
		data['qty'] = i.qty
		data['price_of_sales_invoice'] = i.rate

		last_price_purchase = get_last_purchase_invoice_for_item(i.item_code)

		data['last_price_purchase'] = last_price_purchase
		data['total_of_sales_invoice'] = float(i.qty or 0 ) * float(i.rate or 0)
		total1 += data['total_of_sales_invoice']
		data['diff'] = float(i.rate or 0 ) - float(last_price_purchase or 0)
		total2 += data['diff']
		data['total_diff'] = float(i.qty or 0 ) * (float(i.rate or 0 ) - float(last_price_purchase or 0))
		data['per_diff'] = (float(i.rate or 0) - float(last_price_purchase or 0)) / float(last_price_purchase or 0) * 100
		
		last_three_prices = get_last_sales_invoice_for_item(i.item_code)

		if last_three_prices[0]:
			data['first_last_price'] = last_three_prices[0]['rate']
			data['first_last_date'] = last_three_prices[0]['posting_date']
		
		if last_three_prices[1]:
			data['second_last_price'] = last_three_prices[1]['rate']
			data['second_last_date'] = last_three_prices[1]['posting_date']
		
		if last_three_prices[2]:
			data['third_last_price'] = last_three_prices[2]['rate']
			data['third_last_date'] = last_three_prices[2]['posting_date']
		
		results.append(data)
	results.append(())
	results.append(("","","","","Net Total of Sales Invoice" , doc.net_total))
	results.append(("","","","","Total Rates of Sales with Purchase Price" , total1))
	results.append(("","","","","Total Differante" , total2))
	results.append(("","","","","Percentage of Sales Invoice" , float(total2) / float(total1) * 100))

	return results
		




def get_columns(filters):
	columns = [
		{
			"fieldname": "sales_invoice",
			"label": _("Sales Invoice"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
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
			"fieldname": "price_of_sales_invoice",
			"label": _("Price of Sales Invoice"),
			"fieldtype": "Data",
			"width": 250,
		},
		{
			"fieldname": "last_price_purchase",
			"label": _("Last Price Purchase"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "total_of_sales_invoice",
			"label": _("Total of Sales Invoice"),
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

		{
			"fieldname": "first_last_price",
			"label": _("First Last Price"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "first_last_date",
			"label": _("First Last Date"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "second_last_price",
			"label": _("Second Last Price"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "second_last_date",
			"label": _("Second Last Date"),
			"fieldtype": "Date",
			"width": 100,
		},

		{
			"fieldname": "third_last_price",
			"label": _("Third Last Price"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "third_last_date",
			"label": _("Third Last Date"),
			"fieldtype": "Date",
			"width": 100,
		},
	]
	return columns