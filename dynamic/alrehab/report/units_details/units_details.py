# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, date_diff, flt
from datetime import datetime, date
from frappe.utils import getdate
from dynamic.alrehab.api import get_updates_for_report

def execute(filters=None):
    columns, data = [], []
    
    columns = [
        {"label": _("Unit"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": _("Area"), "fieldname": "unit_area", "fieldtype": "Data", "width": 80},
        {"label": _("Subscription"), "fieldname": "subscription", "fieldtype": "Link", "options": "Subscription", "width": 150},
        {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": _("Invoice Name"), "fieldname": "invoice_name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
        {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
        {"label": _("Subscription Plan"), "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 150},
        {"label": _("Amount"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Invoice Fine %"), "fieldname": "fine_percent", "fieldtype": "Float", "width": 120},
        {"label": _("Delay Days"), "fieldname": "num_of_delay_days", "fieldtype": "Int", "width": 120},
        {"label": _("Invoice Fine Amount"), "fieldname": "deferred_revenue_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Invoice Total Amount after Fine"), "fieldname": "total_with_fine", "fieldtype": "Currency", "width": 120},
        {"label": _("Journal Entry"), "fieldname": "journal_entry", "fieldtype": "Link", "options": "Journal Entry", "width": 150},
        {"label": _("Journal Entry Date"), "fieldname": "journal_entry_date", "fieldtype": "Date", "width": 100},
    ]

    filters_conditions = [" 1 = 1 "]
    if filters.get("customer"):
        filters_conditions.append(f"invoice.customer = '{filters.get('customer')}'")
    if filters.get("sales_invoice"):
        filters_conditions.append(f"invoice.name = '{filters.get('sales_invoice')}'")
    if filters.get("subscription_plan"):
        filters_conditions.append(f"item.item_name = '{filters.get('subscription_plan')}'")
    
    filter_condition = " AND ".join(filters_conditions)
    if not filter_condition:
        filter_condition = ""

    query = f"""
        SELECT
            invoice.docstatus,
            invoice.customer,
            customer.unit_area,
            sub.name AS subscription,
            sub.start_date,
            sub.end_date,
            item.item_name,
            item.amount,
            invoice.name AS invoice_name,
            invoice.posting_date,
            invoice.due_date,
            invoice.status,
            invoice.total,
            invoice.fine_percent,
            invoice.num_of_delay_days,
            invoice.deferred_revenue_amount,
            je.name AS journal_entry,
            je.posting_date AS journal_entry_date
        FROM
            `tabSales Invoice` AS invoice
        LEFT JOIN
            `tabSales Invoice Item` AS item ON item.parent = invoice.name
        LEFT JOIN
            `tabCustomer` AS customer ON customer.name = invoice.customer
        LEFT JOIN
            `tabSubscription Invoice` AS sub_si ON sub_si.invoice = invoice.name
        LEFT JOIN
            `tabSubscription` AS sub ON sub.name = sub_si.parent
        LEFT JOIN
            `tabJournal Entry` AS je ON je.name = (
                SELECT
                    jea.parent
                FROM
                    `tabJournal Entry Account` AS jea
                WHERE
                    jea.reference_name = invoice.name
                LIMIT 1
            )
        WHERE
            {filter_condition}
        ORDER BY
            invoice.customer, sub.name, invoice.name, item.item_name
    """

    result = frappe.db.sql(query, as_dict=1)
    
    
    return columns, result