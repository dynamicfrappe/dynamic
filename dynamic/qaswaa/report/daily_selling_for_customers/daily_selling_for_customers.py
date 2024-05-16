# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import math
from dynamic.future.financial_statements import (
	get_period_list,
	validate_dates , 
	get_months,
)
from frappe.utils import getdate , cint , add_months, get_first_day , add_days 


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)


	return columns, data


def get_data(filters):

	conditions = " AND 1=1"

	if filters.get("customer") :
		conditions += f" and si.customer = '{filters.get('customer')}'"
	if filters.get("sales_person") :
		conditions += f" and st.sales_person = '{filters.get('sales_person')}'"


	sql =  f'''
		SELECT 
			si.customer as customer,
			st.sales_person as sales_person
		FROM 
			`tabSales Invoice` si
		INNER JOIN
			`tabSales Team` st
		ON
			si.name = st.parent
		WHERE 
			si.docstatus = 1
			AND si.posting_date >= '{filters.get('period_start_date')}'
			AND si.posting_date <= '{filters.get('period_end_date')}'
			{conditions}
		GROUP BY 
			si.customer,
			st.sales_person
		'''
	customers = frappe.db.sql(sql , as_dict= 1)


	


	resulte = []
	
	if customers:
		for i in customers:
			data = {}
			sums = {}
			data['customer'] = i.customer
			data['sales_person'] = i.sales_person

			base_grand_total = 0
			net_total = 0
			base_total_taxes_and_charges = 0
			base_total_allocated_amount = 0
			resulte.append(data)

			babe = []
			if filters.get("cost_center") :
				babe.append(('cost_center' , '=' , filters.get('cost_center')))
			if filters.get("warehouse") :
				babe.append(('set_warehouse' , '=' , filters.get('warehouse')))
			if filters.get("sales_partner") :
				babe.append(('sales_partner' , '=' , filters.get('sales_partner')))
			babe.append(("posting_date" , "<=" , filters.get("period_end_date")))
			babe.append(("posting_date" , ">=" , filters.get("period_start_date")))
			
			babe.append(('customer', '=', i.customer))
			babe.append(('is_return', '=', 0))

			temp = frappe.get_list(doctype = "Sales Invoice" , filters = babe , fields = ['*'])
			for j in temp:
				data1 = {}
				data1['posting_date'] = j.posting_date
				data1['name'] = j.name
				data1['cost_center'] = j.cost_center
				data1['warehouse'] = j.set_warehouse
				data1['net_total'] = j.net_total
				data1['base_total_taxes_and_charges'] = j.base_total_taxes_and_charges
				data1['base_grand_total'] = j.base_grand_total
				data1['base_total_allocated_amount'] = j.base_total_allocated_amount


				base_grand_total += j.base_grand_total
				net_total += j.net_total
				base_total_taxes_and_charges += j.base_total_taxes_and_charges
				base_total_allocated_amount = j.base_total_allocated_amount


			

				resulte.append(data1)
			sums['base_grand_total'] = base_grand_total 
			sums['net_total'] = net_total
			sums['base_total_taxes_and_charges'] = base_total_taxes_and_charges
			sums['base_total_allocated_amount'] = base_total_allocated_amount
			sums['sales_person'] = "Total"
			resulte.append(sums)

			
	return resulte

def get_purcashe_invoice_return(sales_invoice):
	sql =  f'''
		SELECT 
			p.name as name
		FROM 
			`tabSales Invoice` p
		WHERE 
			p.is_return = 1
			AND p.return_against = '{sales_invoice}';
		'''
	customer = frappe.db.sql(sql , as_dict= 1)

	return customer[0]['name'] if customer else None


def get_columns(filters):
	columns = [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200,
		},
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Data",
			"width": 200,
		},
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
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
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
			"fieldname": "base_total_allocated_amount",
			"label": _("Total Allocated Amount"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns
