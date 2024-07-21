# gift_stock_report.py
import frappe
from frappe import _

def execute(filters=None):
    
    
    conditions = []
    where_clause = "WHERE se.docstatus = 1 "
    if filters.get("customer"):
        conditions.append("customer = '{}'".format(filters.get("customer")))
        where_clause = where_clause + f"""AND se.customer_id = '{filters.get("customer")}'"""
    if filters.get("cost_center"):
        conditions.append("se.cost_center = '{}'".format(filters.get("cost_center")))
        where_clause = where_clause + f"""AND se.cost_center = '{filters.get("cost_center")}'"""
    if filters.get("item"):
        conditions.append("sed.item_code = '{}'".format(filters.get("item")))
        where_clause = where_clause + f"""AND sed.item_code = '{filters.get("item")}'"""
    if filters.get("t_warehouse"):
        conditions.append("sed.t_warehouse = '{}'".format(filters.get("t_warehouse")))
        where_clause = where_clause + f"""AND sed.t_warehouse = '{filters.get("t_warehouse")}'"""
    if filters.get("s_warehouse"):
        conditions.append("sed.s_warehouse = '{}'".format(filters.get("s_warehouse")))
        where_clause = where_clause + f"""AND sed.s_warehouse = '{filters.get("s_warehouse")}'"""
    if filters.get("from_date"):
        conditions.append("se.posting_date >= '{}'".format(filters.get("from_date")))
        where_clause = where_clause + f"""AND se.posting_date >= '{filters.get("from_date")}'"""
    if filters.get("to_date"):
        conditions.append("se.posting_date <= '{}'".format(filters.get("to_date")))
        where_clause = where_clause + f"""AND se.posting_date <= '{filters.get("to_date")}'"""

    columns = [
        ("Customer") + ":Link/Customer:120",
        ("Transaction") + ":Link/Stock Entry:200",
        ("Item") + ":Link/Item:200",
        ("Stock Entry Type") + "::150",
        ("Total Quantity") + ":Float:100",
        ("Sales Person") + ":Link/Sales Person:120",
        ("Cost Center") + ":Link/Cost Center:100",
        ("Target Warehouse") + ":Link/Warehouse:150",
        ("Source Warehouse") + ":Link/Warehouse:150",
    ]

    dispensing_simples = frappe.db.get_value("Stock Entry Type" , {"matrial_type":"Dispensing Simples"} , 'name')

    main_query = f"""
        SELECT 
            se.customer_id AS customer, 
            se.name AS transaction,
            sed.item_code AS item, 
            se.stock_entry_type, 
            sed.qty AS total_quantity, 
            st.sales_person , 
            se.cost_center , 
            sed.t_warehouse AS "target_warehouse",
            sed.s_warehouse AS "source_warehouse"
        FROM 
            `tabStock Entry` se
        JOIN
            `tabStock Entry Detail` sed ON se.name = sed.parent
        LEFT JOIN
            `tabSales Team` st ON se.name = st.parent
        {where_clause} AND se.stock_entry_type = '{dispensing_simples}'

    """

    gift_transfer_data = frappe.db.sql(main_query, as_dict=True)

    received_simples = frappe.db.get_value("Stock Entry Type" , {"matrial_type":"Received Simples"} , 'name')
    second_query = f"""
        SELECT 
            se.customer_id AS customer, 
            se.name AS transaction,
            sed.item_code AS item, 
            se.stock_entry_type, 
            sed.qty AS total_quantity, 
            st.sales_person ,
            se.cost_center,
            sed.t_warehouse AS "target_warehouse",
            sed.s_warehouse AS "source_warehouse"
        FROM 
            `tabStock Entry` se
        JOIN
            `tabStock Entry Detail` sed ON se.name = sed.parent
        LEFT JOIN
            `tabSales Team` st ON se.name = st.parent
        {where_clause} AND se.stock_entry_type = '{received_simples}'

    """
    get_revieved_data = frappe.db.sql(second_query , as_dict=True)




    if get_revieved_data and gift_transfer_data:
        result = [{'stock_entry_type':'total' , 'total_quantity': get_revieved_data[0]['total_quantity'] - gift_transfer_data[0]['total_quantity']}]
        data = gift_transfer_data + get_revieved_data + result
        return columns, data
    if not get_revieved_data or not gift_transfer_data:
        data = gift_transfer_data + get_revieved_data
        return columns, data



