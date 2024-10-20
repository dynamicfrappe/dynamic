# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data


def get_conditions(filters):
    conditions = " 1=1 "

    from_date, to_date = filters.get("from_date"), filters.get("to_date")
    if from_date and to_date:
        if from_date > to_date:
            frappe.throw("From date should be before to_date.")
    if filters.get("from_date"):
        conditions += f" and SI.posting_date >= '{from_date}'"
    if filters.get("to_date"):
        conditions += f" and SI.posting_date <= '{to_date}'"
    invoice = filters.get("sales_invoice")
    if invoice:
        conditions += f" and SI.name = '{invoice}' "
    sales_person = filters.get("sales_person")
    if sales_person:
        conditions += f" and ST.sales_person = '{sales_person}' "
    item_code = filters.get("item_code")
    if item_code:
        conditions += f" and SII.item_code = '{item_code}' "
    item_group = filters.get("item_group")
    if item_group:
        conditions += f" and SII.item_group = '{item_group}' "

    return conditions

def get_data(filters):

    conditions = get_conditions(filters)
    sql = f'''
        SELECT
            SI.name As sales_invoice,
            ST.sales_person,
            SII.item_code,
            TD.target_qty,
            TD.target_amount,
            (SII.amount * ST.allocated_percentage) /100 As invoice_amount,
            (SII.qty * ST.allocated_percentage) /100 As invoice_qty,
            sum((SII.amount * ST.allocated_percentage) /100) as total_amount,
            sum((SII.qty * ST.allocated_percentage) /100) as total_qty
        
            FROM 
                `tabSales Invoice` SI
            Left JOIN 
                `tabSales Invoice Item` SII
            ON 
                SI.name = SII.parent
            LEFT JOIN
                `tabSales Team` ST
            ON 
                SI.name = ST.parent
            Left Join 
                `tabTarget Detail` TD
            ON 
                TD.parent = ST.sales_person AND TD.item_code = SII.item_code
            WHERE
                {conditions}
            group by item_code, sales_person
    
    '''
    data = frappe.db.sql(sql , as_dict = 1)

    return data

def get_columns(filters):
    columns = [
            {
                "label": _("Sales Invoice"),
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 180,
            },
            {
                "label": _("Item"),
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "width": 180,
            },
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "options": "Sales Person",
                "width": 180,
            },
            {
                "label": _("Target Qty"),
                "fieldname": "target_qty",
                "fieldtype": "Data",
                "width": 140,
            },
            {
                "label": _("Target Amount"),
                "fieldname": "target_amount",
                "fieldtype": "Data",
                "width": 140,
            },
            {
                "label": _("Invoice Item QTY * Contribution %)"),
                "fieldname": "invoice_qty",
                "fieldtype": "Data",
                "width": 140,
            },
            {
                "label": _("Invoice Item Amount * Contribution %"),
                "fieldname": "invoice_amount",
                "fieldtype": "Data",
                "width": 140,
            },
            {
                "label": _("Total Item QTY * Contribution %"),
                "fieldname": "total_amount",
                "fieldtype": "Data",
                "width": 140,
            },
            {
                "label": _("Total Item Amount * Contribution %"),
                "fieldname": "total_qty",
                "fieldtype": "Data",
                "width": 140,
            },
    ]

    return columns