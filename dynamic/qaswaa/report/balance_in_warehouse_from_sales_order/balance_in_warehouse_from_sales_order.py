# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_date()
	return columns, data


def execute(filters=None):
	columns, data = get_columns(), get_date(filters)
	return columns, data

def get_date(filters):
	conditions = " 1=1 "
	
	if filters.get("date") :
		conditions +=f" and SO.delivery_date= '{filters.get('date')}' "

	if filters.get("sales_order") :
		conditions +=f" and SO.name = '{filters.get('sales_order')}' "
	
	if filters.get("customer") :
		conditions +=f" and SO.customer = '{filters.get('customer')}' "

	if filters.get("customer_name") :
		conditions +=f" and SO.customer_name = '{filters.get('customer_name')}' "

	if filters.get("billing_status") :
		conditions +=f" and SO.billing_status = '{filters.get('billing_status')}' "
	
	if filters.get("delivery_status") :
		conditions +=f" and SO.billing_status = '{filters.get('billing_status')}' "


	sql =f'''
			SELECT
				SO.name , SO.customer , SO.customer_name , SO.currency ,
				SO.delivery_date , SO.grand_total , SO.status ,
				SO.per_delivered , SO.per_billed , SO.base_grand_total ,
				SO.order_type ,SO.selling_price_list ,
				SOI.item_code , SOI.item_name, SOI.qty , SOI.warehouse 
			FROM 
				`tabSales Order` SO
			INNER JOIN 
				`tabSales Order Item` SOI
			ON 
				SO.name = SOI.parent
			where
				{conditions}
		'''
	data = frappe.db.sql(sql , as_dict = 1)
	for entry in data :
		res_qty = frappe.db.get_value(
                "Bin",
                {"item_code": entry["item_code"], "warehouse": entry["warehouse"]}, 
				"reserved_qty",
            )
		entry["reserved_qty"] = res_qty		
	# frappe.throw(str(data))
	return data


def get_columns():
	return[
		{
			"fieldname": "name",
			"label": _("ID"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 150,
		},
		{
			"fieldname": "delivery_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150,
		},
		{
			"fieldname": "customer_name",
			"label": _("Customer Name"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 80,
		},
		{
			"fieldname": "grand_total",
			"label": "Grand Total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "per_delivered",
			"label": "Delivered",
			"fieldtype": "Percent",
			"width": 50,
		},
		{
			"fieldname": "per_billed",
			"label": "Billed",
			"fieldtype": "Percent",
			"width": 50,
		},
		{
			"fieldname": "base_grand_total",
			"label": "Grand Total(C0ompany Currency)",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 50,
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"width": 100,
		},
		{
			"fieldname": "order_type",
			"label": _("Order Type"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "selling_price_list",
			"label": _("Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 100,
		},
		{
			"fieldname": "item_code",
			"label": _("Item code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 130,
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"fieldname": "qty",
			"label": _("Qty"),
			"fieldtype": "Data",
			"width": 50,
		},
		{
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 100,
		},
		{
			"fieldname": "reserved_qty",
			"label": _("Total Qty for warehouse"),
			"fieldtype": "Data",
			"width": 50,
		},

	]
