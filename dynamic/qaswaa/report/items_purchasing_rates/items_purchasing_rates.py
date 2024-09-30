# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe

def get_data(filters=None):

    conditions = " 1=1 "

    if filters.get("item"):
        conditions += f""" AND pi.item_code = '{filters.get("item")}'"""
    
    if filters.get("item_name"):
        conditions += f""" AND pi.item_name = '{filters.get("item_name")}'"""
    
    if filters.get("supplier_name"):
        conditions += f""" AND s.supplier_name = '{filters.get("supplier_name")}'"""
    
    if filters.get("supplier"):
        conditions += f""" AND p.supplier = '{filters.get("supplier")}'"""
    
    if filters.get("date_from"):
        conditions += f""" AND p.posting_date >= '{filters.get("date_from")}'"""
    
    if filters.get("date_to"):
        conditions += f""" AND p.posting_date <= '{filters.get("date_to")}'"""

    query = f"""
        SELECT 
            i.item_code,
            i.item_name,
            pi.rate AS last_purchased_rate,
            p.name AS invoice,
            p.posting_date,
            p.supplier,
            s.supplier_name
        FROM 
            `tabPurchase Invoice Item` pi
        JOIN 
            `tabItem` i ON pi.item_code = i.item_code
        JOIN 
            `tabPurchase Invoice` p ON pi.parent = p.name
        JOIN 
            `tabSupplier` s ON p.supplier = s.name
        WHERE 
            pi.docstatus = 1
            AND p.posting_date = (
                SELECT MAX(posting_date) 
                FROM `tabPurchase Invoice` 
                WHERE name = p.name
            )
            AND {conditions}
        GROUP BY 
            i.item_code
    """
    # Execute the query with filters
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
            "label": "Last Purchased Rate",
            "fieldname": "last_purchased_rate",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Invoice",
            "fieldname": "invoice",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 150
        },
        {
            "label": "Posting Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Supplier",
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "label": "Supplier Name",
            "fieldname": "supplier_name",
            "fieldtype": "Data",
            "width": 200
        }
    ]

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
