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
			posting_date , name , customer , base_grand_total ,
 			set_warehouse , selling_price_list , cost_center , payment_terms_template,
			total , discount_amount , paid_amount , additional_discount_percentage , outstanding_amount
		FROM 
			`tabSales Invoice`
		WHERE 
			{conditions}
		'''
	data = frappe.db.sql(sql , as_dict = 1)
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
		s =  f'''
		SELECT 
			(name) as policy_document , delivered_date , charged_date,shipping_company , 
			 policy_number , delivery_number 
		FROM 
			`tabSales Document States`
		WHERE 
			invoice_name = '{entry["name"]}'
		'''
		sales_document = frappe.db.sql(s , as_dict = 1)
		if sales_document :
			entry["delivered_date"] = sales_document[0]["delivered_date"]
			entry["charged_date"] = sales_document[0]["charged_date"]

			entry["shipping_company"] = sales_document[0]["shipping_company"]
			entry["policy_document"] = sales_document[0]["policy_document"]
			entry["delivery_number"] = sales_document[0]["delivery_number"]

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
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 300,
		},
		{
			"fieldname": "base_grand_total",
			"label": "Grand Total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "total",
			"label": "Total",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "discount_amount",
			"label": "Discount Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "paid_amount",
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
		},
		{
			"fieldname": "additional_discount_percentage",
			"label": "Additional Discount Percentage",
			"fieldtype": "Float",
			"width": 150,
		},
				{
			"fieldname": "discount_amount",
			"label": "Additional Discount Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "delivered_date",
			"label": _("Delivered Date"),
			"fieldtype": "Date",
			"width": 300,
		},
		{
			"fieldname": "charged_date",
			"label": _("Charged Date"),
			"fieldtype": "Date",
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
		},		
		{
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
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
			"fieldname": "selling_price_list",
			"label": _("Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 300,
		},
		{
			"fieldname": "shipping_company",
			"label": _("Shipping Company"),
			"fieldtype": "Link",
			"options": "Shipping Company",
			"width": 300,
		},
		{
			"fieldname": "policy_document",
			"label": _("Policy Document"),
			"fieldtype": "Link",
			"options": "Sales Document States",
			"width": 300,
		},
		{
			"fieldname": "delivery_number",
			"label": _("Delivery Number"),
			"fieldtype": "Check",
			"width": 300,
		}
	]
	return columns
