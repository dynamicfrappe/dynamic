# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    
    columns = [
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 120},
        {"label": _("Unit Area"), "fieldname": "unit_area", "fieldtype": "Data", "width": 60},
        {"label": _("Invoice Name"), "fieldname": "invoice_name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": _("Subscription Plan"), "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": _("Amount"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
        {"label": _("Invoice Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Invoice Fine %"), "fieldname": "fine_percent", "fieldtype": "Currency", "width": 120},
        {"label": _("Delay Days"), "fieldname": "num_of_delay_days", "fieldtype": "Int", "width": 120},
        {"label": _("Invoice Fine Amount"), "fieldname": "deferred_revenue_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Invoice Total Amount after Fine"), "fieldname": "total_with_fine", "fieldtype": "Currency", "width": 120},
    ]

    filters_conditions = []
    if filters.get("customer"):
        filters_conditions.append(f"invoice.customer = '{filters.get('customer')}'")
    if filters.get("sales_invoice"):
        filters_conditions.append(f"invoice.name = '{filters.get('sales_invoice')}'")
    if filters.get("subscription_plan"):
        filters_conditions.append(f"item.item_name = '{filters.get('subscription_plan')}'")
    
    filter_condition = " AND ".join(filters_conditions)
    if filter_condition:
        filter_condition = " AND " + filter_condition
    else:
        filter_condition = ""

    query = f"""
        SELECT
            invoice.customer,
            customer.unit_area,
            item.item_name,
            item.amount,
            invoice.name AS invoice_name,
            invoice.status,
            invoice.total,
            invoice.fine_percent,
            invoice.num_of_delay_days,
            invoice.deferred_revenue_amount,
            (invoice.deferred_revenue_amount + invoice.total) as total_with_fine
        FROM
            `tabSales Invoice` AS invoice
        LEFT JOIN
            `tabSales Invoice Item` AS item ON item.parent = invoice.name
        LEFT JOIN
            `tabCustomer` AS customer ON customer.name = invoice.customer
        WHERE
            invoice.docstatus = 1
            {filter_condition}
        ORDER BY
            invoice.customer, invoice.posting_date DESC
    """

    result = frappe.db.sql(query, as_dict=1)
    
    # Organize data into a hierarchical structure
    previous_customer = None
    previous_invoice = None
    for row in result:
        # Add a new row for the customer group if it's a new customer
        if row['customer'] != previous_customer:
            data.append({
                "customer": row['customer'],
                "unit_area": row['unit_area'],
                "indent": 0,   
                "group": 1  
            })
            previous_customer = row['customer']
            previous_invoice = None
        
        # Add a new row for the invoice group if it's a new invoice
        if row['invoice_name'] != previous_invoice:
            data.append({
                "invoice_name": row['invoice_name'],
                "status": row['status'],
                "total": row['total'],
                "fine_percent": row['fine_percent'],
                "num_of_delay_days": row['num_of_delay_days'],
                "deferred_revenue_amount": row['deferred_revenue_amount'],
                "total_with_fine": row['total_with_fine'],
                "indent": 1,
                "group": 1  
            })
            previous_invoice = row['invoice_name']
        
        # Add the subscription plan details under the invoice
        data.append({
            "item_name": row['item_name'],
            "total": row['amount'],
            "indent": 2    
        })

    return columns, data

