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
			SII.sales_order , SII.rate , SII.price_list_rate ,
			(SII.rate - SII.price_list_rate) as diffrance , 
			((SII.rate - SII.price_list_rate) / 100 ) as diffrance_percentage ,
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
		group by 
			SII.item_code , SI.customer
	'''
	data = frappe.db.sql(sql , as_dict = 1)
	return data

def get_columns():
	return[
		{ 
            "label": _("Customer"), 
            "fieldname": "customer", 
            "fieldtype": "Link", 
            "options": "Customer", 
            "width": 300, 
        },
		{ 
            "label": _("Item Code"), 
            "fieldname": "item_code", 
            "fieldtype": "Link", 
            "options": "Item", 
            "width": 300, 
        }, 
		{ 
            "label": _("Sales Order"), 
            "fieldname": "sales_order", 
            "fieldtype": "Link", 
            "options": "Sales Order", 
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
            "label": _("Rate"), 
            "fieldname": "rate", 
            "fieldtype": "Currency",
			"options": "currency",  
            "width": 200, 
        },
		{ 
            "label": _("Price List Rate"), 
            "fieldname": "price_list_rate", 
            "fieldtype": "Currency",
			"options": "currency",  
            "width": 200, 
        },
		{ 
            "label": _("Amount"), 
            "fieldname": "amount", 
            "fieldtype": "Currency",
			"options": "currency",  
            "width": 200, 
        },
		{ 
            "label": _("Diffrance"), 
            "fieldname": "diffrance", 
            "fieldtype": "Currency",
			"options": "currency",  
            "width": 200, 
        },
		{ 
            "label": _("Diffrance percentage"), 
            "fieldname": "diffrance_percentage", 
            "fieldtype": "Currency",
			"options": "currency",  
            "width": 200, 
        },
	]