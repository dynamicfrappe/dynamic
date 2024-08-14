# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

# import frappe
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
        conditions += f" and Q.transaction_date >= '{from_date}'"
    if to_date:
        conditions += f" and Q.transaction_date <= '{to_date}'" 
    if filters.get("quotation"):
        conditions += f" and Q.name = '{filters.get('quotation')}' "
    if filters.get("party_name"):
        conditions += f" and Q.party_name = '{filters.get('party_name')}' "
    if filters.get("cost_center"):
        conditions += f" and Q.cost_center = '{filters.get('cost_center')}' "
    if filters.get("warehouse"):
        conditions += f" and QI.warehouse = '{filters.get('warehouse')}' "
    if filters.get("sales_person"):
        conditions += f" and ST.sales_person = '{filters.get('sales_person')}' "
    return conditions



def get_relevent_warehouses(filters = None):
    conditions = get_conditions(filters)
    sql = frappe.db.sql(f'''
            SELECT 
                QI.item_code
            FROM 
                `tabQuotation` Q
            INNER JOIN 
                `tabQuotation Item` QI
            ON 
                Q.name = QI.parent
            LEFT JOIN
                `tabSales Team` ST
            ON 
                Q.name = ST.parent
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
                Q.name As quotation, QI.item_code , QI.item_name, QI.qty, Q.warehouse , Q.cost_center
            FROM 
                `tabQuotation` Q
            INNER JOIN 
                `tabQuotation Item` QI
            ON 
                Q.name = QI.parent
            LEFT JOIN
                `tabSales Team` ST
            ON 
                Q.name = ST.parent
            WHERE
                {conditions}
            
        '''
    quotation_items = frappe.db.sql(sql , as_dict = 1)

    data = []

    # Fetch stock balance for each item and relevant warehouse
    for item in quotation_items:
        row = {
            "name": item.quotation,
            "item_code": item.item_code,
            "item_name": item.item_name,
            "qty": item.qty,
            "warehouse": item.warehouse,
            'cost_center':item.cost_center
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
            "label": _("ID"),
            "fieldtype": "Link",
            "options": "Quotation",
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
            "fieldname": "cost_center",
            "label": _("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center",
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
            "width": 100
        })
    return columns