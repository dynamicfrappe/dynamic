# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1 "
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    sales_order = filters.get("sales_order")
    item_code = filters.get("item_code")
    customer = filters.get("customer")
    cost_center = filters.get("cost_center")
    set_warehouse = filters.get("set_warehouse")

    if from_date:
        conditions += f" AND so.transaction_date >= '{from_date}'"
    if to_date:
        conditions += f" AND so.transaction_date <= '{to_date}'"
    if customer:
        conditions += f" AND so.customer = '{customer}'"
    if cost_center:
        conditions += f" AND so.cost_center = '{cost_center}'"        
    if item_code:
        conditions += f" AND soi.item_code = '{item_code}'"
    if set_warehouse:
        conditions += f" AND so.set_warehouse = '{set_warehouse}'"
    if sales_order:
        conditions += f" AND so.name = '{sales_order}'"    
    sql = f'''
        SELECT 
            so.name AS sales_order,
            so.customer,
            so.transaction_date,
            soi.item_code,
            soi.item_name,
            soi.qty AS sales_qty,
            soi.net_rate,
            sre.available_qty_to_reserve AS available_qty,
            sre.reserved_qty,
            (sre.reserved_qty + soi.qty) - sre.available_qty_to_reserve AS residual_qty
        FROM 
            `tabSales Order` so
        INNER JOIN
            `tabSales Order Item` soi ON soi.parent = so.name
        INNER JOIN
            `tabStock Reservation Entry` sre ON sre.voucher_no = so.name
        WHERE
            so.reserve_stock = 1 AND
            so.set_warehouse = sre.warehouse AND
            soi.item_code = sre.item_code AND {conditions}
    '''
    data = frappe.db.sql(sql, as_dict=1)
    return data




def get_columns(filters):
    columns = [
        {
            "fieldname": "sales_order",
            "label": _("Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 300,
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 300,
        },
        {
            "fieldname": "transaction_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 300,
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "net_rate",
            "label": _("Net Rate"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "sales_qty",
            "label": _("Sales Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "reserved_qty",
            "label": _("Reserved Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "available_qty",
            "label": _("Available Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "residual_qty",
            "label": _("Residual Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
	]
    return columns