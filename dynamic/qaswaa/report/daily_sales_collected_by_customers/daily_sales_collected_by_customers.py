# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_data(filters):
	final_data = []
	sql = '''
		SELECT customer , sales_partner
		FROM
			`tabSales Invoice`
		GROUP BY 
			customer'''
	customers = frappe.db.sql(sql , as_dict = 1)
	conditions = " 1=1"
	if filters.get("from_date"):
		conditions += f" and posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" and posting_date <= '{filters.get('to_date')}'"
	if filters.get("customer"):
		customers = [{"customer" : filters.get("customer")}]
	if filters.get("cost_center"):
		conditions += f" and cost_center = '{filters.get('cost_center')}'"
	if filters.get("warehouse"):
		conditions += f" and set_warehouse = '{filters.get('warehouse')}'"
	if filters.get("sales_partner"):
		conditions += f" and sales_partner = '{filters.get('sales_partner')}'"
	for customer in customers :
		final_data.append({"customer" :f'{customer["customer"]}' , "sales_partner" : f'{customer["sales_partner"]}'})
		s = f'''
		SELECT 
			posting_date , name , set_warehouse ,
			selling_price_list , cost_center , payment_terms_template,
			base_total , base_total_taxes_and_charges , base_grand_total ,
			base_paid_amount , outstanding_amount  
		FROM 
			`tabSales Invoice`
		WHERE 
			customer = '{customer["customer"]}'
			and 
			{conditions}
		'''
		data = frappe.db.sql(s , as_dict = 1)
		for entry in data :
			sql1 = f'''
					select
						st.sales_person
					from
						`tabSales Team` st
					inner join 
						`tabSales Invoice` si
					on 
						st.parent = si.name
					where
						si.name = '{entry["name"]}'  
					'''
			sales_person = frappe.db.sql(sql1, as_dict = 1)
			if sales_person :
				entry["sales_person"] = sales_person[0]["sales_person"]
			
			final_data.append(entry)
	return final_data

def get_columns():
	columns = [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 300,
		},
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 300,
		},
		{
			"fieldname": "payment_terms_template",
			"label": _("Payment Terms Template"),
			"fieldtype": "Link",
			"options": "Payment Terms Template",
			"width": 300,
		},		{
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 300,
		},		{
			"fieldname": "selling_price_list",
			"label": _("Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 300,
		},
		{
			"fieldname": "posting_date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 300,
		},
		{
			"fieldname": "sales_partner",
			"label": _("Sales Partner"),
			"fieldtype": "Link",
			"options": "Sales Partner",
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