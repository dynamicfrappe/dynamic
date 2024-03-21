# gift_stock_report.py

import frappe
from frappe import _

def execute(filters=None):
    columns = [
        _("Customer") + ":Link/Customer:120",
        _("Transaction") + ":Link/Stock Entry:200",
        _("Item") + ":Link/Item:250",
        _("Stock Entry Type") + "::150",
        _("Total Quantity") + ":Float:120",
        _("Sales Person") + ":Link/Sales Person:120",
    ]
    
    # Initialize filters
    conditions = []
    if filters.get("customer"):
        conditions.append("customer = '{}'".format(filters.get("customer")))
    if filters.get("from_date"):
        conditions.append("posting_date >= '{}'".format(filters.get("from_date")))
    if filters.get("to_date"):
        conditions.append("posting_date <= '{}'".format(filters.get("to_date")))
    
    # Construct the WHERE clause
    where_clause = " AND ".join(conditions)

    # Query to fetch data for 'gift transfer' and 'gift received' separately
    gift_transfer_data = frappe.db.sql("""
        SELECT 
            se.customer_id, 
            se.name AS transaction,
            sed.item_code AS item, 
            se.stock_entry_type, 
            SUM(sed.qty) AS total_quantity, 
            st.sales_person 
        FROM 
            `tabStock Entry` AS se
        JOIN
            `tabStock Entry Detail` AS sed ON se.name = sed.parent
        LEFT JOIN
            `tabSales Team` AS st ON se.name = st.parent
        WHERE 
            se.docstatus = 1 
            AND se.stock_entry_type = 'صرف عينات'
            AND ({where_clause})
        GROUP BY 
            se.customer, 
            se.stock_entry_type
    """.format(where_clause=where_clause), as_dict=True)


    gift_received_data = frappe.db.sql("""
        SELECT 
            se.customer_id, 
            se.name AS transaction,
            sed.item_code AS item, 
            se.stock_entry_type, 
            SUM(sed.qty) AS total_quantity, 
            st.sales_person 
        FROM 
            `tabStock Entry` AS se
        JOIN
            `tabStock Entry Detail` AS sed ON se.name = sed.parent
        LEFT JOIN
            `tabSales Team` AS st ON se.name = st.parent
        WHERE 
            se.docstatus = 1 
            AND se.stock_entry_type = 'استلام عينات'
            AND ({where_clause})
        GROUP BY 
            se.customer, 
            se.stock_entry_type
    """.format(where_clause=where_clause), as_dict=True)
    if gift_received_data and gift_transfer_data:
        result = [{'stock_entry_type':'total' , 'total_quantity': gift_received_data[0]['total_quantity'] - gift_transfer_data[0]['total_quantity']}]
        data = gift_transfer_data + gift_received_data + result
        return columns, data
    if not gift_received_data or not gift_transfer_data:
        data = gift_transfer_data + gift_received_data
        return columns, data



