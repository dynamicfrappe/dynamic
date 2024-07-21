# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    
    return columns, data

def get_columns(filters):
    columns = [
        #1
        {
            "label": _("Invoice Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        #2
        {
            "label": _("Invoice"),
            "fieldname": "sales_invoice_name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120
        },
        #3
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 200
        },
        #4
        {
            "label": _("Customer"),
            "fieldname": "customer_name",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120
        },
        #5
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200
        },
        #6
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        #7
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Float",
            "width": 120
        },
        #8
        {
            "label": _("QTY"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 120
        },
        #9
        {
            "label": _("Delivered Qty"),
            "fieldname": "delivered_qty",
            "fieldtype": "Float",
            "width": 120
        },
        #10
        {
            "label": _("Difference"),
            "fieldname": "difference",
            "fieldtype": "Float",
            "width": 120
        },
    ]
    return columns

def get_data(filters):

    data = []

    conditions = '1=1 '
    if filters.get('from_date') and filters.get('to_date'):
        conditions += f" and date(`tabSales Invoice`.posting_date) BETWEEN date('{filters.get('from_date')}') AND date('{filters.get('to_date')}')"
    else:
        if filters.get('from_date'):
            conditions += f" and date(`tabSales Invoice`.posting_date) >= date('{filters.get('from_date')}')"
        if filters.get('to_date'):
            conditions += f" and date(`tabSales Invoice`.posting_date) <= date('{filters.get('to_date')}')"
    if filters.get('invoice'):
        conditions += " AND `tabSales Invoice`.name = '%s' "%(filters.get('invoice'))
    if filters.get('cost_center'):
        conditions += " AND `tabSales Invoice`.cost_center = '%s' "%(filters.get('cost_center'))
    if filters.get('warehouse'):
        conditions += " AND `tabSales Invoice`.set_warehouse = '%s' "%(filters.get('warehouse'))
    if filters.get('customer'):
        conditions += " AND `tabSales Invoice`.customer = '%s' "%(filters.get('customer'))
    if filters.get('sales_person'):
        conditions += " AND `tabSales Team`.sales_person = '%s' "%(filters.get('sales_person'))
    if filters.get('item_code'):
        conditions += " AND `tabSales Invoice Item`.item_code = '%s' "%(filters.get('item_code'))
    if filters.get('item_group'):
        conditions += " AND `tabSales Invoice Item`.item_group = '%s' "%(filters.get('item_group'))
    

    sql = f'''
        Select
            `tabSales Invoice`.posting_date,
            `tabSales Invoice`.name AS sales_invoice_name,
            `tabSales Invoice`.set_warehouse AS warehouse,
            `tabSales Invoice`.customer_name,
            `tabSales Invoice Item`.item_code,
            `tabSales Invoice Item`.item_name,
            `tabSales Invoice Item`.amount,
            `tabSales Invoice Item`.qty,
            `tabSales Invoice Item`.delivered_qty,
            (`tabSales Invoice Item`.qty - `tabSales Invoice Item`.delivered_qty) AS difference
        From
            `tabSales Invoice` `tabSales Invoice`
        Inner Join
            `tabSales Invoice Item` 
        On 
            `tabSales Invoice`.name = `tabSales Invoice Item`.parent
        Left Join
            `tabSales Team`
        ON 
            `tabSales Invoice`.name = `tabSales Team`.parent 
        
        Where 
            {conditions}
        
    '''
    
    data = frappe.db.sql(sql,as_dict=1)
    total_amount =sum([float(row.get("amount") or 0) for  row in data])
  
    
    data.append({"item_name":"Total" ,"amount" : total_amount })
    
    return data




