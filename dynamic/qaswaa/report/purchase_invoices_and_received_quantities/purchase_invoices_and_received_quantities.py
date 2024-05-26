# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):

    conditions = "1=1"

    invoice = filters.get("purchase_invoice")
    if invoice:
        conditions += f" AND pi.name = '{invoice}'"
    supplier = filters.get("supplier")
    if supplier:
        conditions += f" AND pi.supplier = '{supplier}'"
    warehouse = filters.get("warehouse")
    if warehouse:
        conditions += f" AND pii.warehouse = '{warehouse}'"
    item_group = filters.get('item_group')
    if item_group:
        conditions += f" AND pii.item_group = '{item_group}'"
    item = filters.get("item_code")
    if item:
        conditions += f" AND pii.item_code = '{item}'"

    sql = f'''
        SELECT
            pi.name, 
            pi.due_date, 
            pi.supplier,
            pii.item_code,
            pii.item_name,
            pii.net_amount,
            pii.qty,
            pii.received_qty,
            (pii.qty - pii.received_qty) as difference
        FROM
            `tabPurchase Invoice` pi
        LEFT JOIN
            `tabPurchase Invoice Item` pii
        ON 
            pi.name = pii.parent
        WHERE
            {conditions}
    '''
        
    data = frappe.db.sql(sql, as_dict=True)
    return data

def get_columns():

    columns = [
        {
            "label": _("ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 200,
        },
        { 
            "label": _("Date"), 
            "fieldname": "due_date", 
            "fieldtype": "Date",
            "width": 200, 
        }, 
        { 
            "label": _("Supplier"), 
            "fieldname": "supplier", 
            "fieldtype": "Link", 
            "options": "Supplier", 
            "width": 200, 
        },
        { 
            "label": _("Item Code"), 
            "fieldname": "item_code", 
            "fieldtype": "Link", 
            "options": "Item", 
            "width": 200,
        },
        { 
            "label": _("Item Name"), 
            "fieldname": "item_name", 
            "fieldtype": "Data", 
            "width": 300, 
        },
        { 
            "label": _("Net Amount"), 
            "fieldname": "net_amount", 
            "fieldtype": "Currency",
            "options":"currency", 
            "width": 200, 
        },
        { 
            "label": _("Accepted Qty"), 
            "fieldname": "qty", 
            "fieldtype": "Float", 
            "width": 200, 
        },
        { 
            "label": _("Received Qty"), 
            "fieldname": "received_qty", 
            "fieldtype": "Float", 
            "width": 200, 
        },
        { 
            "label": _("Difference"), 
            "fieldname": "difference", 
            "fieldtype": "Float", 
            "width": 200, 
        },
    ]
    
    return columns