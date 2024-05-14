# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters):

	start_date = filters.get("start_date")
	end_date = filters.get("end_date")

	cost_center = filters.get("cost_center")

	conditions = []

	conditions.append(('posting_date' , '>=' , start_date))
	conditions.append(('posting_date' , '<=' , end_date))
	conditions.append(('cost_center' , '=' , cost_center))


	if filters.get("warehouse") :
		conditions.append(('set_warehouse' , '=' , filters.get('warehouse')))
		
	if filters.get("customer") :
		conditions.append(('customer' , '=' , filters.get('customer')))

	if filters.get("sales_person") :
		conditions.append(('sales_person' , '=' , filters.get('sales_person')))

	if filters.get("sales_partner") :
		conditions.append(('sales_partner' , '=' , filters.get('sales_partner')))

	resulte = []
	invoices = frappe.db.get_list( "Sales Invoice", filters=conditions)

	for invoice in invoices:
		doc = frappe.get_doc("Sales Invoice" , invoice.name)
		temp = {}
		temp['posting_date'] = doc.posting_date
		temp['name'] = invoice.name
		temp['warehouse'] = doc.set_warehouse
		temp['customer'] = doc.customer
		temp['net_total'] = doc.net_total
		temp['base_total_taxes_and_charges'] = doc.base_total_taxes_and_charges
		temp['base_grand_total'] = doc.base_grand_total
		temp['total_advance'] = doc.total_advance
		num = frappe.db.get_value("Sales Invoice" , {"is_return": 1, "return_against": invoice.name},'base_grand_total') if not None else 0
		if num:
			temp['refund'] = num
			temp['diff'] = float(doc.base_grand_total or 0 ) - (float(doc.total_advance or 0 ) + float(num or 0))
		resulte.append(temp)

	
	return resulte

def get_columns(filters):
	columns = [
		{
			"fieldname": "posting_date",
			"label": _("Date"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "name",
			"label": _("Serial"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200,
		},
		{
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 200,
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200,
		},	
		{
			"fieldname": "net_total",
			"label": _("Total"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "base_total_taxes_and_charges",
			"label": _("Total Taxes And Charges"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "base_grand_total",
			"label": _("Grand Total"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "total_advance",
			"label": _("Total Allocated Amount"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "refund",
			"label": _("Refund"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "diff",
			"label": _("Differante"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns