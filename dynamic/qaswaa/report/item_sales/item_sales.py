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
		conditions += f" and SI.posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" and SI.posting_date <= '{filters.get('to_date')}'"
	if filters.get("customer"):
		conditions += f" and SI.customer = '{filters.get('customer')}'"
	if filters.get("item_code"):
		conditions += f" and SII.item_code = '{filters.get('item_code')}'"
	if filters.get("item_group"):
		conditions += f" and SII.item_group = '{filters.get('item_group')}'"
	

	sql = f'''
		SELECT
			SI.customer , 
			SII.item_code,
			SII.item_name,
			SUM(SII.qty) as qty,
			SUM(SII.amount) as amount
		FROM
			`tabSales Invoice` SI
		LEFT JOIN
			`tabSales Invoice Item` SII
		ON 
			SI.name = SII.parent
		WHERE
			SI.docstatus = 1 and {conditions}
	'''
	data = frappe.db.sql(sql , as_dict = 1)
	return data

def get_columns():
	return[
		{ 
            "label": _("Item Code"), 
            "fieldname": "item_code", 
            "fieldtype": "Link", 
            "options": "Item", 
            "width": 300, 
        }, 
        { 
            "label": _("Item Name"), 
            "fieldname": "item_name", 
            "fieldtype": "Data", 
            "width": 200, 
        },
		{ 
            "label": _("Qty"), 
            "fieldname": "qty", 
            "fieldtype": "Data", 
            "width": 200, 
        }, 
		{ 
            "label": _("Amount"), 
            "fieldname": "amount", 
            "fieldtype": "Currency",
			"options": "currency",  
            "width": 200, 
        },
	]