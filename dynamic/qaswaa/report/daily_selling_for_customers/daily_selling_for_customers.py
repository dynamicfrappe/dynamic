# # Copyright (c) 2024, Dynamic and contributors
# # For license information, please see license.txt

import frappe
from frappe import _
import math
from dynamic.future.financial_statements import (
	get_period_list,
	validate_dates , 
	get_months,
)
from frappe.utils import getdate , cint , add_months, get_first_day , add_days 


def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data



def get_data(filters):
    data = []
    customers = frappe.get_all("Customer", fields=["name","customer_group","territory"])

    for customer_idx, customer in enumerate(customers):
        customer_name = customer.get("name")
        customer_group = customer.get("customer_group")
        sales_invoices_filters = {
            "customer": customer_name,
            "docstatus": ["!=", 2],
            "is_return": 0
        }
        
        if filters.get("cost_center"):
           sales_invoices_filters['cost_center'] = [ "=", filters.get("cost_center")]
        if filters.get("sales_person"):
           sales_invoices_filters['sales_person'] = [ "=", filters.get("sales_person")]
        if filters.get("sales_partner"):
           sales_invoices_filters['sales_partner'] = [ "=", filters.get("sales_partner")]   
        if filters.get("customer_name"):
           sales_invoices_filters['customer_name'] = [ "=", filters.get("customer_name")]
        if filters.get("set_warehouse"):
           sales_invoices_filters['set_warehouse'] = [ "=", filters.get("set_warehouse")]   
                 
        if filters.get("start_date") and filters.get("end_date"):
            sales_invoices_filters["posting_date"] = ["between", [filters.get("start_date"), filters.get("end_date")]]
        elif filters.get("start_date") and not filters.get("end_date"):
            sales_invoices_filters["posting_date"] = [">=", filters.get("start_date")]
        elif filters.get("end_date") and not filters.get("start_date"):
            sales_invoices_filters["posting_date"] = ["<=", filters.get("end_date")]
        if filters.get("status"):
           status = filters.get("status")
           sales_invoices_filters['status'] = ['in', status]
        if filters.get("customer_group"):
            sales_invoices_filters['customer_group'] = ["=", filters.get("customer_group")]
        if filters.get("territory"):
            sales_invoices_filters['territory'] = ["=", filters.get("territory")]    

        sales_invoices = frappe.get_all("Sales Invoice", filters=sales_invoices_filters, fields=["name", "posting_date", "set_warehouse","net_total", "base_total_taxes_and_charges", "grand_total","outstanding_amount","status"])
        customer_data = []
        total_refund_amount = 0
        total_advance_amount = 0 

        for idx, invoice in enumerate(sales_invoices):
            invoice_name = invoice.get("name")
            posting_date = invoice.get("posting_date")
            warehouse = invoice.get("set_warehouse")
            net_total = invoice.get("net_total")
            base_total_taxes_and_charges = invoice.get("base_total_taxes_and_charges")
            grand_total = invoice.get("grand_total")
            diff = invoice.get("outstanding_amount")
            status = invoice.get("status")

            
            sales_person = frappe.db.get_value("Sales Team", {"parent": invoice_name, "parenttype": "Sales Invoice", "parentfield": "sales_team"}, "sales_person")

            refund_amount = frappe.db.get_value("Sales Invoice", {"is_return": 1, "return_against": invoice_name}, 'base_grand_total') or 0
            total_refund_amount += refund_amount

            total_advance = 0
            mode_of_payment = None
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Sales Invoice"}, fields=["allocated_amount"])
            for entry in payment_entries:
                total_advance += entry.get("allocated_amount")
            total_advance_amount += total_advance
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Sales Invoice"}, fields=["parent"])
            for entry in payment_entries:
                payment_entry = frappe.get_doc("Payment Entry", entry.get("parent"))
                mode_of_payment = payment_entry.mode_of_payment if payment_entry.mode_of_payment else None
            
            
            if idx == 0:
                customer_data.append({
                    "customer_name": customer_name,
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "set_warehouse": warehouse,
                    "net_total": net_total,
                    "status":status,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "refund_amount": refund_amount,
                    "total_advance_amount": total_advance,
                    "diff": diff,
                    "sales_person": sales_person,
                    "mode_of_payment": mode_of_payment
                })
            else:
                customer_data.append({
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "set_warehouse": warehouse,
                    "net_total": net_total,
                    "status":status,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "refund_amount": refund_amount,
                    "total_advance_amount": total_advance,
                    "diff": diff,
                    "sales_person": sales_person,
                    "mode_of_payment": mode_of_payment
                })

        data.extend(customer_data)
    if customer_data:
        total_grand_total = sum([invoice.get("grand_total", 0) for invoice in sales_invoices])
        total_base_total_taxes_and_charges = sum([invoice.get("base_total_taxes_and_charges", 0) for invoice in sales_invoices])
        total_net_total = sum([invoice.get("net_total", 0) for invoice in sales_invoices])
        data.append({
            "customer_name": "",
            "invoice_name": "",
            "posting_date": "",
            "set_warehouse": "",
            "net_total": total_net_total,
            "base_total_taxes_and_charges": total_base_total_taxes_and_charges,
            "grand_total": total_grand_total,
            "refund_amount": total_refund_amount ,
            "total_advance_amount": total_advance_amount ,
            "diff": diff ,
        })
        data.append({})


    return data



def get_columns(filters):
    
    columns = [
        {
            "label": "Customer Name", 
            "fieldname": "customer_name", 
            "fieldtype": "Link", 
            "options": "Customer"
        },
        
        {
            "label": "Invoice Name", 
            "fieldname": "invoice_name", 
            "fieldtype": "Link", 
            "options": "Sales Invoice"
        },
        {
            "label": "Posting Date", 
            "fieldname": "posting_date", 
            "fieldtype": "Date"
        },
        {
            "label": "Warehouse", 
            "fieldname": "set_warehouse", 
            "fieldtype": "Link", 
            "options": "Warehouse"
        },
        {
            "label": "Sales Person", 
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person"
        },
        {
            "label":"Status",
            "fieldname":"status",
            "fieldtype":"Select",
            "options":"\nDraft\nReturn\nCredit Note Issued\nSubmitted\nPaid\nPartly Paid\nUnpaid\nUnpaid and Discounted\nPartly Paid and Discounted\nOverdue and Discounted\nOverdue\nCancelled\nInternal Transfer"
        },
        {
            "label": "Mode of Payment", 
            "fieldname": "mode_of_payment",
            "fieldtype": "Link",
            "options": "Mode of Payment"
        },
        {
            "fieldname": "net_total",
            "fieldtype": "Currency",
            "label":"Net Total",
            "options":"currency",
            "width": 200,
        },
        {
            "fieldname": "base_total_taxes_and_charges",
            "label":"Total Taxes",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Grand Total", 
            "fieldname": "grand_total", 
            "fieldtype": "Currency"
        },
        {
            "label": "Total Advance", 
            "fieldname": "total_advance_amount", 
            "fieldtype": "Currency"
        },
        {
            "fieldname": "refund_amount",
            "fieldtype": "Currency",
            "label":"Refund",
            "width": 200,
        },
        {
            "fieldname": "diff",
            "fieldtype": "Currency",
            "label":"Diff",
            "width": 200,
        },
        
    ]
    
    return columns


        









