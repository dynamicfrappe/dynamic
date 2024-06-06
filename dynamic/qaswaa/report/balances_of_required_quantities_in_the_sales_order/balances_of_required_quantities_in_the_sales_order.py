

import frappe
from frappe import _
from erpnext.stock.utils import get_stock_balance

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data


def get_columns(filters=None):
    columns = [
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
    ]

    
    # columns.append({
    #             "fieldname": f"{balance_warehouse}",
    #             "label": _(f"Balance Warehouse"),
    #             "fieldtype": "Data",
    #             "width": 100,
    #         })

    return columns



# def get_data(filters):
#     orders_with_items = []

#     if filters.get("item_code"):
#         filters['item_code'] = ["=", filters.get("item_code")]

#     sales_orders = frappe.get_all("Sales Order", filters=filters, fields=["name"])

#     for order in sales_orders:
#         order_items = frappe.get_all("Sales Order Item",
#                                      filters={"parent": order.name},
#                                      fields=["item_code", "item_name", "qty", "warehouse"])
#         for item in order_items:
#             actual_qty = frappe.db.sql("""
#                 SELECT SUM(actual_qty)
#                 FROM `tabBin`
#                 WHERE item_code = %s AND warehouse = %s
#             """, (item.item_code, item.warehouse))[0][0] or 0
#             orders_with_items.append({
#                 "name": order.name,
#                 "item_code": item.item_code,
#                 "item_name": item.item_name,
#                 "qty": item.qty,
#                 "sales_warehouse": item.warehouse,
#                 "sales_balance": actual_qty,
#             })

#     return orders_with_items



def get_data(filters):
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
                
                data.append({f"balance_{warehouse}": item})
            elif stock_balance == 0 and item['sales_warehouse'] == warehouse:
                item['sales_balance'] = 0
                data.append({f"balance_{warehouse}": item})

    return data







