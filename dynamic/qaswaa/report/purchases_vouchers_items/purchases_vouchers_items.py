# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe

def get_data(filters=None):
    query = """
        SELECT 
            i.item_code,
            i.item_name,
            pi.posting_date,
            pi.name as invoice,
            pi.cost_center,
            pi.set_warehouse as warehouse,
            s.name AS supplier,
            pi_item.qty AS qty,
            pi_item.rate AS net_rate,
            (pi_item.qty * pi_item.rate) AS total,
            pi.status
        FROM 
            `tabPurchase Invoice` pi
        JOIN 
            `tabPurchase Invoice Item` pi_item ON pi.name = pi_item.parent
        JOIN 
            `tabItem` i ON pi_item.item_code = i.item_code
        JOIN 
            `tabSupplier` s ON pi.supplier = s.name
        WHERE 
            pi.docstatus = 1
    """

    conditions = []

    if filters.get("item_code"):
        conditions.append("i.item_code = %(item_code)s")
    
    if filters.get("supplier"):
        conditions.append("s.name = %(supplier)s")
    
    if filters.get("item_group"):
        conditions.append("i.item_group = %(item_group)s")
    
    if filters.get("cost_center"):
        conditions.append("pi.cost_center = %(cost_center)s")
    
    if filters.get("warehouse"):
        conditions.append("pi.set_warehouse = %(warehouse)s")
    
    if filters.get("date_from"):
        conditions.append("(pi.posting_date >= %(date_from)s)")
    
    if filters.get("date_to"):
        conditions.append("(pi.posting_date <= %(date_to)s)")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    data = frappe.db.sql(query, filters, as_dict=True)
    return data

def get_columns():
    return [
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Invoice",
            "fieldname": "invoice",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 150
        },
        {
            "label": "Cost Center",
            "fieldname": "cost_center",
            "fieldtype": "Link",
            "options": "Cost Center",
            "width": 150
        },
        {
            "label": "Warehouse",
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150
        },
        {
            "label": "Supplier",
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "label": "Qty",
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "Net Rate",
            "fieldname": "net_rate",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Total",
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        }
    ]

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
