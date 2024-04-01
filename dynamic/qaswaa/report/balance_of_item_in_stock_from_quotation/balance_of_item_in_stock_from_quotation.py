# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_date(filters)
	return columns, data

def get_date(filters):
	conditions = " 1=1 "
	
	if filters.get("date") :
		conditions +=f" and Q.transaction_date= '{filters.get('date')}' "

	if filters.get("quotation_to") :
		conditions +=f" and Q.quotation_to = '{filters.get('quotation_to')}' "
	
	if filters.get("party_name") :
		conditions +=f" and Q.party_name = '{filters.get('party_name')}' "

	if filters.get("customer_name") :
		conditions +=f" and Q.customer_name = '{filters.get('customer_name')}' "

	if filters.get("warehouse") :
		conditions +=f" and QI.warehouse = '{filters.get('warehouse')}' "

	if filters.get("quotation") :
		conditions +=f" and Q.name = '{filters.get('quotation')}' "

	if filters.get("price_list") :
		conditions +=f" and Q.selling_price_list = '{filters.get('price_list')}' "


	sql =f'''
			SELECT
				Q.name , Q.party_name , Q.transaction_date , Q.grand_total ,
				Q.status , Q.currency , Q.selling_price_list ,Q.quotation_to , 
				Q.customer_name, QI.item_code , QI.item_name, QI.qty , QI.warehouse
			FROM 
				`tabQuotation` Q
			INNER JOIN 
				`tabQuotation Item` QI
			ON 
				Q.name = QI.parent
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
	return data


def get_columns():
	return[
		{
			"fieldname": "name",
			"label": _("ID"),
			"fieldtype": "Link",
			"options": "Quotation",
			"width": 200,
		},
		{
			"fieldname": "transaction_date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Select",
			"width": 100,
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 200,
		},
		{
			"fieldname": "selling_price_list",
			"label": _("Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 200,
		},
		{
			"fieldname": "quotation_to",
			"label": _("Quotation To"),
			"fieldtype": "Link",
			"options": "DocType"
		},
		{
			"fieldname": "party_name",
			"label": _("Party Name"),
			"fieldtype": "Dynamic Link",
			"options": "quotation_to",
			"width": 200,
		},
		{
			"fieldname": "customer_name",
			"label": _("Customer Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "item_code",
			"label": _("Item code"),
			"fieldtype": "Link",
			"options": "Item",
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
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 200,
		},
		{
			"fieldname": "grand_total",
			"label": "Grand Total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "reserved_qty",
			"label": _("Total Qty for warehouse"),
			"fieldtype": "Data",
			"width": 50,
		},

	]
