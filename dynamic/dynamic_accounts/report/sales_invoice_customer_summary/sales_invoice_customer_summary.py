# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters or {})
    data = get_data(filters or {})
    return columns, data




def get_data(filters):
    conditions = get_conditios(filters)
    sql = f"""
        SELECT `tabSales Invoice`.name invoice,`tabSales Invoice`.posting_date , `tabSales Invoice Item`.item_code,
            `tabSales Invoice Item`.qty,`tabSales Invoice Item`.rate ,
            (`tabSales Invoice Item`.qty * `tabSales Invoice Item`.rate) total_sales,
            `tabStock Ledger Entry`.valuation_rate cost,
            (`tabStock Ledger Entry`.valuation_rate * `tabSales Invoice Item`.qty) total_cost,
            ((`tabSales Invoice Item`.qty * `tabSales Invoice Item`.rate) - (`tabStock Ledger Entry`.valuation_rate * `tabSales Invoice Item`.qty))profit,
            `tabSales Invoice`.customer 
            ,`tabSales Team`.sales_person ,
            `tabSales Invoice`.territory,
            `tabSales Invoice Item`.`item_name`, `tabSales Invoice Item`.`item_group`,
            `tabSales Invoice`.customer_name
        from `tabSales Invoice`
        INNER JOIN `tabSales Invoice Item`
            ON `tabSales Invoice`.name = `tabSales Invoice Item`.parent
        INNER JOIN `tabStock Ledger Entry`
            ON `tabStock Ledger Entry`.item_code = `tabSales Invoice Item`.item_code
        INNER JOIN `tabSales Team`
        ON `tabSales Team`.parent =  `tabSales Invoice`.name  AND `tabSales Team`.parent = `tabSales Invoice Item`.parent
        where  `tabSales Invoice`.docstatus = 1 {conditions}
        group by `tabSales Invoice`.name, `tabSales Invoice Item`.item_code ,`tabSales Invoice`.customer
        order by `tabSales Invoice`.name desc
        """
    sql = frappe.db.sql(sql,as_dict=1)
    return sql

def get_conditios(filters):
    conditions = ' AND 1=1 '
    if filters.get('from_date') and filters.get('to_date'):
        conditions += f" and date(`tabSales Invoice`.posting_date) BETWEEN date('{filters.get('from_date')}') AND date('{filters.get('to_date')}')"
    else:
        if filters.get('from_date'):
            conditions += f" and date(`tabSales Invoice`.posting_date) >= date('{filters.get('from_date')}')"
        if filters.get('to_date'):
            conditions += f" and date(`tabSales Invoice`.posting_date) <= date('{filters.get('to_date')}')"
    if filters.get('customer'):
        conditions += " AND `tabSales Invoice`.customer = '%s' "%(filters.get('customer'))
    if filters.get('item_code'):
        conditions += " AND `tabSales Invoice Item`.item_code = '%s' "%(filters.get('item_code'))
    if filters.get('warehouse'):
        conditions += " AND `tabSales Invoice`.set_warehouse = '%s' "%(filters.get('warehouse'))
    if filters.get('invoice'):
        conditions += " AND `tabSales Invoice`.name = '%s' "%(filters.get('invoice'))
    if filters.get('sales_person'):
        conditions += " AND `tabSales Team`.sales_person = '%s' "%(filters.get('sales_person'))
    if filters.get('cost_center'):
        conditions += " AND `tabSales Invoice`.cost_center = '%s' "%(filters.get('cost_center'))
    if filters.get('sales_partner'):
        conditions += " AND `tabSales Invoice`.sales_partner = '%s' "%(filters.get('sales_partner'))
    
    

    
    return conditions


def get_columns(filters):
    columns = [
        {
            "label": _("Invoice"),
            "fieldname": "invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 250
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 120
        },
        {
            "label": _("Invoice Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 120
        },
         {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Total Sales"),
            "fieldname": "total_sales",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Cost(Valuation Rate)"),
            "fieldname": "cost",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Total Cost"),
            "fieldname": "total_cost",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Profit"),
            "fieldname": "profit",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 120
        },
        {
            "label": _("Territory"),
            "fieldname": "territory",
            "fieldtype": "Data",
            "width": 120
        },

    ]
    return columns
        