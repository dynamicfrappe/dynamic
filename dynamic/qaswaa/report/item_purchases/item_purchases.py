# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1 "
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    item_code = filters.get("item_code")
    item_group = filters.get("item_group")
    supplier = filters.get("supplier")
    cost_center = filters.get("cost_center")
    warehouse = filters.get("warehouse")

    if from_date:
        conditions += f""" AND p.posting_date >= date('{from_date}')"""
    if to_date:
        conditions += f""" AND p.posting_date <= date('{to_date}')"""
    if supplier:
        conditions += f""" AND p.supplier = '{supplier}'"""
    if cost_center:
        conditions += f""" AND p.cost_center = '{cost_center}'"""        
    if item_code:
        conditions += f""" AND pi.item_code = '{item_code}'"""
    if warehouse:
        conditions += f""" AND pi.warehouse = '{warehouse}'"""    
    if item_group:
        conditions += f""" AND i.item_group = '{item_group}'"""

    data = frappe.db.sql(f"""
        SELECT pi.item_code, pi.item_name, 
               SUM(CASE WHEN p.status != 'Return' THEN pi.qty ELSE 0 END) as qty_difference1,
               SUM(CASE WHEN p.status = 'Return' THEN pi.qty ELSE 0 END) as qty_difference2,
               (SUM(CASE WHEN p.status != 'Return' THEN pi.qty ELSE 0 END) +
                SUM(CASE WHEN p.status = 'Return' THEN pi.qty ELSE 0 END)) as qty_difference,
               SUM(CASE WHEN p.status != 'Return' THEN pi.net_amount ELSE 0 END) as net_amount_difference1,
               SUM(CASE WHEN p.status = 'Return' THEN pi.net_amount ELSE 0 END) as net_amount_difference2,
               (SUM(CASE WHEN p.status != 'Return' THEN pi.net_amount ELSE 0 END) +
                SUM(CASE WHEN p.status = 'Return' THEN pi.net_amount ELSE 0 END)) as net_amount_difference                             
        FROM `tabPurchase Invoice` p
        INNER JOIN `tabPurchase Invoice Item` pi ON p.name = pi.parent
        INNER JOIN `tabItem` i ON pi.item_code = i.name
        WHERE {conditions} AND p.docstatus != 2
        GROUP BY pi.item_code
    """, as_dict=True)

    return data
def get_columns():
    return [
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
            "width": 300, 
        },
        {
            "label": _("Quantity"), 
            "fieldname": "qty_difference", 
            "fieldtype": "Float",
            "width": 200, 
        },
        {
            "label": _("Amount"), 
            "fieldname": "net_amount_difference", 
            "fieldtype": "Currency",
            "options":"currency",
            "width": 200, 
        },
    ]
