

import frappe
from frappe import _
from erpnext.stock.utils import get_stock_balance

def execute(filters=None):
	columns, data = get_columns(), get_date(filters)
	return columns, data



def get_columns():
    return[
        {
            "fieldname": "name",
            "label": _("ID"),
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
            "width": 50,
        },
            {
            "fieldname": "sales_warehouse",
            "label": _("Sales Warehouse"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "sales_balance",
            "label": _("Sales Balance"),
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "balance_warehouse",
            "label": _("Balance Warehouse"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "stock_balance",
            "label": _("Stock Balance"),
            "fieldtype": "Data",
            "width": 100,
        }
    ]

def get_date(filters):
    conditions = "1=1"
    data = []

    if filters.get("sales_order"):
        conditions += f" and Q.name = '{filters.get('sales_order')}' "
    if filters.get("customer"):
        conditions += f" and Q.customer = '{filters.get('customer')}' "
    
    if filters.get("cost_center"):
        conditions += f" and Q.cost_center = '{filters.get('cost_center')}' "   
    
    warehouses = frappe.get_all("Warehouse", filters={"disabled": 0}, pluck="name")

    for warehouse in warehouses:
        if filters.get("warehouse"):
            conditions += f" and QI.warehouse = '{filters.get('warehouse')}' "

        sql = f'''
            SELECT
                Q.name, QI.item_code, QI.item_name, QI.qty, QI.warehouse as sales_warehouse
            FROM 
                `tabSales Order` Q
            INNER JOIN 
                `tabSales Order Item` QI
            ON 
                Q.name = QI.parent
            WHERE {conditions}    
        '''

        warehouse_data = frappe.db.sql(sql, as_dict=1)

        for item in warehouse_data:
            stock_balance = get_stock_balance(item['item_code'], warehouse)
            if stock_balance > 0:
                item['stock_balance'] = stock_balance
                item['balance_warehouse'] = warehouse
                item['sales_balance'] = stock_balance if item['sales_warehouse'] == warehouse else 0
                data.append(item)
            elif stock_balance == 0 and item['sales_warehouse'] == warehouse:
                item['sales_balance'] = 0
                data.append(item)

    return data







