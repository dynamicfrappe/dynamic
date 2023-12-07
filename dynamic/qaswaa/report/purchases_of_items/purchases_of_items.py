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
		conditions += f" and PI.posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" and PI.posting_date <= '{filters.get('to_date')}'"
	if filters.get("supplier"):
		conditions += f" and PI.supplier = '{filters.get('supplier')}'"
	if filters.get("item_code"):
		conditions += f" and PII.item_code = '{filters.get('item_code')}'"
	if filters.get("item_group"):
		conditions += f" and PII.item_group = '{filters.get('item_group')}'"
	

	sql = f'''
		SELECT
			PI.supplier , 
			PII.item_code,
			PII.item_name,
			SUM(PII.qty) as qty,
			SUM(PII.amount) as amount
		FROM
			`tabPurchase Invoice` PI
		INNER JOIN
			`tabPurchase Invoice Item` PII
		ON 
			PI.name = PII.parent
		WHERE
			PI.docstatus = 1 and {conditions}
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
            "width": 250, 
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
