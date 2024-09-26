# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	# Define columns for the report
	columns = get_columns()
	
	# Fetch the data
	data = get_data(filters)
	
	return columns, data

def get_columns():
	return [
		{"label": _("Supplier"), "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 150},
		{"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 150},
		{"label": _("Purchase Quantity"), "fieldname": "purchase_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Avg Purchase Rate"), "fieldname": "avg_purchase_rate", "fieldtype": "Currency", "width": 120},
		{"label": _("Total Purchase Amount"), "fieldname": "purchase_amount", "fieldtype": "Currency", "width": 150},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
		{"label": _("Customer Name"), "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
		{"label": _("Sales Quantity"), "fieldname": "sales_qty", "fieldtype": "Float", "width": 120},
		{"label": _("Avg Sales Rate"), "fieldname": "avg_sales_rate", "fieldtype": "Currency", "width": 120},
		{"label": _("Total Sales Amount"), "fieldname": "sales_amount", "fieldtype": "Currency", "width": 150}
	]

def get_data(filters):
	conditions = "1 = 1"
	values = {}

	if filters.get("from_date"):
		conditions += " AND pi.posting_date >= %(from_date)s"
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions += " AND pi.posting_date <= %(to_date)s"
		values["to_date"] = filters["to_date"]
	if filters.get("supplier"):
		conditions += " AND pi.supplier = %(supplier)s"
		values["supplier"] = filters["supplier"]
	if filters.get("item_code"):
		conditions += " AND pii.item_code = %(item_code)s"
		values["item_code"] = filters["item_code"]

	result = frappe.db.sql(f"""
		SELECT 
			pi.supplier AS supplier, 
			pii.item_code AS item_code, 
			pii.item_name AS item_name,
			SUM(pii.qty) AS purchase_qty,
			AVG(pii.rate) AS avg_purchase_rate,
			SUM(pii.amount) AS purchase_amount,
			si.customer AS customer,
			si.customer_name AS customer_name,
			SUM(sii.qty) AS sales_qty,
			AVG(sii.rate) AS avg_sales_rate,
			SUM(sii.amount) AS sales_amount
		FROM 
			`tabPurchase Invoice Item` pii
		JOIN 
			`tabPurchase Invoice` pi ON pi.name = pii.parent
		LEFT JOIN 
			`tabSales Invoice Item` sii ON sii.item_code = pii.item_code
		LEFT JOIN 
			`tabSales Invoice` si ON si.name = sii.parent
		WHERE 
			pi.docstatus = 1 AND si.docstatus = 1 AND {conditions} 
		GROUP BY 
			pi.supplier, pii.item_code, si.customer
	""", values, as_dict=True)

	data = []
	previous_supplier = None
	previous_item_code = None

	for row in result:
		
		if row['supplier'] != previous_supplier:
			data.append({
				"supplier": row['supplier'],
				"indent": 0,
				"group": 1 
			})
			previous_supplier = row['supplier']
			previous_item_code = None

		
		if row['item_code'] != previous_item_code:
			data.append({
				"item_code": row['item_code'],
				"item_name": row['item_name'],
				"purchase_qty": row['purchase_qty'],
				"avg_purchase_rate": row['avg_purchase_rate'],
				"purchase_amount": row['purchase_amount'],
				"indent": 1, 
				"group": 1  
			})
			previous_item_code = row['item_code']

		
		if row['customer']: 
			data.append({
				"customer": row['customer'],
				"customer_name": row['customer_name'],
				"sales_qty": row['sales_qty'],
				"avg_sales_rate": row['avg_sales_rate'],
				"sales_amount": row['sales_amount'],
				"indent": 2,  
				"group": 0  
			})

	return data