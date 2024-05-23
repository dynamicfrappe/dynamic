# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_last_purchase_invoice_for_item



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1"
    
    if filters.get("customer"):
        conditions += f" AND so.customer = '{filters.get('customer')}'"
    if filters.get("sales_order"):
        conditions += f" AND so.name = '{filters.get('sales_order')}'"
    if filters.get("set_warehouse"):
        conditions += f" AND so.set_warehouse = '{filters.get('set_warehouse')}'"
    if filters.get("selling_price_list"):
        conditions += f" AND so.selling_price_list = '{filters.get('selling_price_list')}'"    
    if filters.get("from_date"):
        conditions += f" AND so.transaction_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND so.transaction_date <= '{filters.get('to_date')}'"
    if filters.get("cost_center"):
        conditions += f" AND so.cost_center = '{filters.get('cost_center')}'"
    if filters.get("sales_person"):
        conditions += f" AND sales_team.sales_person = '{filters.get('sales_person')}'"

    sql = f'''
        SELECT 
            so.name AS sales_order,
            item.item_code,
            item.item_name,
            item.qty,
            item.rate,
            bin.valuation_rate AS average_cost,
            item.qty * bin.valuation_rate AS total_cost,
            item.rate - bin.valuation_rate AS variance,
            item.qty * (item.rate - bin.valuation_rate) AS total_variance,
            ((item.rate - bin.valuation_rate) / bin.valuation_rate) * 100 AS variance_percentage 
        FROM 
            `tabSales Order` so
        INNER JOIN
            `tabSales Order Item` item ON item.parent = so.name
        LEFT JOIN
            `tabBin` bin ON bin.item_code = item.item_code
                AND bin.warehouse = so.set_warehouse
        LEFT JOIN
            `tabSales Team` sales_team ON sales_team.parent = so.name
        WHERE {conditions}
    '''

    data = frappe.db.sql(sql, as_dict=1)
    return data




def get_columns():
    columns = [
        {
            "fieldname": "sales_order",
            "label": _("Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
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
            "fieldname": "qty",
            "label": _("Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "rate",
            "label": _("Selling price"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "average_cost",
            "label": _("Average Cost"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_cost",
            "label": _("Total Cost"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "variance",
            "label": _("Variance"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_variance",
            "label": _("Total Variance"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "variance_percentage",
            "label": _("Variance Percentage"),
            "fieldtype": "Percent",
            "width": 100,
        },
    ]
    return columns



