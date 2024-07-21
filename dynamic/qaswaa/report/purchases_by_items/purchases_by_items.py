# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data
def get_data(filters):
    conditions = "1=1"
    if filters.get("supplier"):
        conditions += f" AND pi.supplier = '{filters.get('supplier')}'"
    if filters.get("from_date"):
        conditions += f" AND pi.posting_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND pi.posting_date <= '{filters.get('to_date')}'"
    if filters.get("item_group"):
        conditions += f" AND pii1.item_group = '{filters.get('item_group')}'"
    if filters.get("item_code"):
        conditions += f" AND pii1.item_code = '{filters.get('item_code')}'"

    sql = f'''
        SELECT
            pi.name, 
            pii1.item_code,
            pii1.item_name,
            pii1.qty,
            pii1.net_amount
        FROM
            `tabPurchase Invoice` pi
        LEFT JOIN
            `tabPurchase Invoice Item` pii1
        ON 
            pi.name = pii1.parent
        WHERE
            {conditions}
    '''

    data = frappe.db.sql(sql, as_dict=True)
    return data




def get_columns():
    return [
        {
            "fieldname": "name",
            "label": _("ID"),
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 200,
        },
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
            "label": _("Accepted Qty"), 
            "fieldname": "qty", 
            "fieldtype": "Float", 
            "width": 200, 
        },
        { 
            "label": _("Net Amount"), 
            "fieldname": "net_amount", 
            "fieldtype": "Currency",
            "options":"currency", 
            "width": 200, 
        },
    ]