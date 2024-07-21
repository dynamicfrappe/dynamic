# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data
def get_data(filters):
	conditions = " 1=1"
	if filters.get("from_date"):
		conditions += f" and posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" and posting_date <= '{filters.get('to_date')}'"
	if filters.get("customer"):
		conditions += f" and customer = '{filters.get('customer')}'"
	if filters.get("cost_center"):
		conditions += f" and cost_center = '{filters.get('cost_center')}'"
	if filters.get("warehouse"):
		conditions += f" and set_warehouse = '{filters.get('warehouse')}'"
	if filters.get("sales_partner"):
		conditions += f" and sales_partner = '{filters.get('sales_partner')}'"
	
	sql = f'''
		SELECT 
			posting_date , name , set_warehouse , customer ,
			base_total , base_total_taxes_and_charges , base_grand_total ,
			base_paid_amount , outstanding_amount  
		FROM 
			`tabSales Invoice`
		WHERE 
			{conditions}
		'''
	data = frappe.db.sql(sql , as_dict = 1)
	# frappe.throw(str(data))
	for entry in data :
		entry["sales_invoice"] = "Sales Invoice"
	return data

def get_columns():
	columns = [
		{
			"fieldname": "posting_date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 300,
		},
		{
			"fieldname": "name",
			"label": _("Sales Invoice"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 300,
		},
		{
			"fieldname": "set_warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 300,
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 300,
		},
		{
			"fieldname": "sales_invoice",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"fieldname": "base_total",
			"label": "Total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "base_total_taxes_and_charges",
			"label": "Taxes and Charges",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "base_grand_total",
			"label": "Grand Total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "base_paid_amount",
			"label": "Paid Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "outstanding_amount",
			"label": "Outstanding Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		}
	]
	return columns