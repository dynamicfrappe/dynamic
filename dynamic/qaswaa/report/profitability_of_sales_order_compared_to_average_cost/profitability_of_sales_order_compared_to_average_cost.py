# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_last_purchase_invoice_for_item



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    summary = get_report_summary(data)
    return columns, data, None, None, summary

def get_report_summary(data):
    if not data:
        return None

    total_rate = round(sum([float(row.get("selling_price_per_qty") or 0) for  row in data]),2)
    total_of_total_cost = round(sum([float(row.get("total_cost") or 0) for  row in data]),2)
    total_variance  = round(sum([float(row.get("total_variance") or 0) for  row in data]),2)
    ratio = calc_ratio(total_of_total_cost, total_variance)
    return[
        {
            'value' : total_rate,
            'indicator' : 'Blue',
            'label' : _('Total Rate'),
            'datatype' : 'Currency',
        },
        {
            'value' : total_of_total_cost,
            'indicator' : 'Blue',
            'label' :  _('Total Of Average Cost'),
            'datatype' : 'Currency',
        },
        {
            'value' : total_variance,
            'indicator' : 'Green' if total_variance > 0 else 'Red',
            'label' : _('Total Variance'),
            'datatype' : 'Currency',
        },
        {
            'value' : ratio,
            'indicator' : 'Green' if ratio > 0 else 'Red',
            'label' : _('Ratio'),
            'datatype' : 'Percent',
        }
    ]

def calc_ratio(total_of_total_cost, total_variance):
    ratio = 0.0
    if total_of_total_cost:
        ratio  = (total_variance/total_of_total_cost) *100
    else:
        frappe.msgprint("Total Of Average Cost is Zero. Can't calculate the ratio.")
    return ratio


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
            item.rate * item.qty AS selling_price_per_qty,
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
            "fieldname": "selling_price_per_qty",
            "label": _("Selling Price Per Qty"),
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



