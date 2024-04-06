# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_date(filters)
	return columns, data

def get_date(filters):
	conditions = " 1=1 "
	condition = " 1=1 "
	if filters.get("customer") :
		conditions +=f" and so.customer = '{filters.get('customer')}' "
		
	if filters.get("warehouse") :
		conditions +=f" and soi.warehouse = '{filters.get('warehouse')}' "
		condition +=f" and PII.warehouse = '{filters.get('warehouse')}' "

	if filters.get("sales_order") :
		conditions +=f" and so.name = '{filters.get('sales_order')}' "

	if filters.get("price_list") :
		conditions +=f" and so.selling_price_list = '{filters.get('price_list')}' "

	if filters.get("sales_person") :
		conditions +=f" and ST.sales_person = '{filters.get('sales_person')}' "
	
	if filters.get("date") :
		condition +=f" and PI.posting_date = '{filters.get('date')}' "


	sql =f'''
			SELECT
				so.name , soi.item_code , soi.item_name, soi.qty ,
				soi.price_list_rate , soi.rate , soi.discount_amount ,
				(soi.rate - soi.discount_amount) as differance_amount ,
				(soi.rate - soi.discount_amount) / 100 as differance_percentage
			FROM 
				`tabSales Order` so
			INNER JOIN 
				`tabSales Order Item` soi
			ON 
				so.name = soi.parent
			LEFT JOIN 
				`tabSales Team` ST
			ON 
				so.name = ST.parent
			WHERE 
				{conditions}
		'''
	data = frappe.db.sql(sql , as_dict = 1)
	for entry in data :
		entry["sales_rate"]  = 0
		sql =f'''
				SELECT
					PII.rate
				FROM 
					`tabPurchase Invoice Item` PII
				INNER JOIN 
					`tabPurchase Invoice` PI 
				ON
					PI.name = PII.parent
				WHERE 
					PII.item_code = '{entry["item_code"]}' 
					and
					{condition}
				LIMIT 1
			'''
		if frappe.db.sql(sql , as_dict = 1)  :
			sales_rate = frappe.db.sql(sql , as_dict = 1) 
			entry["sales_rate"] = sales_rate[0]["rate"]
		entry["total_sales"] = entry["qty"] * entry["sales_rate"] 
		entry["differance"] = entry["differance_amount"] - entry["sales_rate"]
		entry["total_differance"] = entry["qty"] * entry["differance"]
		if entry["sales_rate"] :
			entry["differance_percentage"] = str(entry["differance"] / entry["sales_rate"] *100) + "%"
	return data

def get_columns():
	return[
		{
			"fieldname": "name",
			"label": _("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 200,
		},
		{
			"fieldname": "item_code",
			"label": _("Item code"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"fieldname": "qty",
			"label": _("Qty"),
			"fieldtype": "Data",
			"width": 50,
		},
		{
			"fieldname": "price_list_rate",
			"label": "Price List Rate",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "rate",
			"label": "Rate",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "discount_amount",
			"label": "Discount Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "differance_amount",
			"label": "Differance Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
				{
			"fieldname": "differance_percentage",
			"label": "Differance Percentage",
			"fieldtype": "Percent",
			"width": 100,
		},
		{
			"fieldname": "sales_rate",
			"label": "Sales Rate",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "total_sales",
			"label": "Total Sales",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "differance",
			"label": "Differance",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "total_differance",
			"label": "Total Differance",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "differance_percentage",
			"label": _("Differance Percentage"),
			"fieldtype": "Data",
			"width": 100,
		}
	]



