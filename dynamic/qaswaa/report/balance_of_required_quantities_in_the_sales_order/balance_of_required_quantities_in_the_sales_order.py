# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):

    relevant_warehouses = get_relevent_warehouses(filters)

    columns = get_columns(relevant_warehouses, filters)

    data = get_data(relevant_warehouses, filters)

    return columns, data

def get_conditions(filters):
    conditions = " 1=1 "
    
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if from_date:
        conditions += f" and SO.transaction_date >= '{from_date}'"
    if to_date:
        conditions += f" and SO.transaction_date <= '{to_date}'" 
    if filters.get("sales_order"):
        conditions += f" and SO.name = '{filters.get('sales_order')}' "
    if filters.get("customer"):
        conditions += f" and SO.customer = '{filters.get('customer')}' "
    if filters.get("cost_center"):
        conditions += f" and SO.cost_center = '{filters.get('cost_center')}' "
    if filters.get("warehouse"):
        conditions += f" and SOI.warehouse = '{filters.get('warehouse')}' "
    if filters.get("sales_person"):
        conditions += f" and ST.sales_person = '{filters.get('sales_person')}' "
    return conditions

def get_relevent_warehouses(filters = None):
    conditions = get_conditions(filters)
    sql = frappe.db.sql(f'''
            SELECT 
                SOI.item_code
            FROM 
                `tabSales Order` SO
            INNER JOIN 
                `tabSales Order Item` SOI
            ON 
                SO.name = SOI.parent
            LEFT JOIN
                `tabSales Team` ST
            ON 
                SO.name = ST.parent
            WHERE
                {conditions}
        ''', as_dict=True)

    item_codes = [item['item_code'] for item in sql]
    if not item_codes:
        return []

    format_strings = ','.join(['%s'] * len(item_codes))
    warehouses = frappe.db.sql(f'''
        SELECT DISTINCT warehouse
        FROM `tabBin`
        WHERE item_code IN ({format_strings})
        AND warehouse IN (SELECT name FROM `tabWarehouse` WHERE is_group = 0)
    ''', item_codes, as_dict=True)

    return [w['warehouse'] for w in warehouses]

def get_data(relevant_warehouses, filters=None):

    conditions = get_conditions(filters)
        
    sql = f'''
            SELECT
                SO.name, SOI.item_code , SOI.item_name, SOI.qty, SOI.warehouse
            FROM 
                `tabSales Order` SO
            INNER JOIN 
                `tabSales Order Item` SOI
            ON 
                SO.name = SOI.parent
            LEFT JOIN
                `tabSales Team` ST
            ON 
                SO.name = ST.parent
            WHERE
                {conditions}
            
        '''
    sales_order_items = frappe.db.sql(sql , as_dict = 1)

    data = []

    # Fetch stock balance for each item and relevant warehouse
    for item in sales_order_items:
        row = {
            "name": item.name,
            "item_code": item.item_code,
            "item_name": item.item_name,
            "qty": item.qty,
            "warehouse": item.warehouse
        }
        balance = frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": item.warehouse}, "actual_qty")
        row["balance"] = balance if balance else 0

        for warehouse in relevant_warehouses:
            balance = frappe.db.get_value("Bin", {"item_code": item.item_code, "warehouse": warehouse}, "actual_qty")
            row[frappe.scrub(warehouse)] = balance if balance is not None and balance >= 0.0 else ""

        data.append(row)

    return data


def get_columns(relevant_warehouses, filters=None):
    columns = [
        {
            "fieldname": "name",
            "label": _("Sales Order ID"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 200,
        },
        {
            "fieldname": "item_code",
            "label": _("Item code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 300,
        },
        {
            "fieldname": "qty",
            "label": _("Qty"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "warehouse",
            "label": _("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 200,
        },
        {
            "fieldname": "balance",
            "label": _("Balance"),
            "fieldtype": "Data",
            "width": 100,
        },
    ]

    # Add dynamic columns for each relevant warehouse
    for warehouse in relevant_warehouses:
        columns.append({
            "fieldname": frappe.scrub(warehouse),
            "label": warehouse,
            "fieldtype": "Data",
            "width": 150
        })
    return columns