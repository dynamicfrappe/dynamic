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
    customers = frappe.get_all("Customer", fields=["name"])

    for customer_idx, customer in enumerate(customers):
        customer_name = customer.get("name")
        sales_invoices_filters = {
            "customer": customer_name,
            "docstatus": ["!=", 2],
            "is_return": 0,
        }
        
        if filters.get("cost_center"):
            sales_invoices_filters['cost_center'] = ["=", filters.get("cost_center")]
        if filters.get("sales_person"):
            sales_invoices_filters['sales_person'] = ["=", filters.get("sales_person")]
        if filters.get("sales_partner"):
            sales_invoices_filters['sales_partner'] = ["=", filters.get("sales_partner")]   
        if filters.get("customer_name"):
            sales_invoices_filters['customer_name'] = ["=", filters.get("customer_name")]
        if filters.get("set_warehouse"):
            sales_invoices_filters['set_warehouse'] = ["=", filters.get("set_warehouse")]   
                 
        if filters.get("start_date") and filters.get("end_date"):
            sales_invoices_filters["posting_date"] = ["between", [filters.get("start_date"), filters.get("end_date")]]
        elif filters.get("start_date") and not filters.get("end_date"):
            sales_invoices_filters["posting_date"] = [">=", filters.get("start_date")]
        elif filters.get("end_date") and not filters.get("start_date"):
            sales_invoices_filters["posting_date"] = ["<=", filters.get("end_date")]
        if filters.get("status"):
            status = filters.get("status")
            sales_invoices_filters['status'] = ['in', status]
        sales_invoices_filters['status'] = ['not in', ['Draft', 'Cancelled']]                      
        
        sales_invoices = frappe.get_all("Sales Invoice", filters=sales_invoices_filters, fields=["name", "posting_date", "set_warehouse", "net_total", "base_total_taxes_and_charges", "grand_total", "outstanding_amount","status"])
        
        customer_data = []
        total_refund_amount = 0
        total_advance_amount = 0
        total_diff = 0
        total_net_total = 0
        total_base_total_taxes_and_charges = 0
        total_grand_total = 0
        sales_invoice_refund = ''
        total_amount_deduction = 0
        

        for idx, invoice in enumerate(sales_invoices):
            invoice_name = invoice.get("name")
            posting_date = invoice.get("posting_date")
            warehouse = invoice.get("set_warehouse")
            net_total = invoice.get("net_total")
            status = invoice.get("status")
            base_total_taxes_and_charges = invoice.get("base_total_taxes_and_charges")
            grand_total = invoice.get("grand_total")
            diff = invoice.get("outstanding_amount")

            sales_person = frappe.db.get_value("Sales Team", {"parent": invoice_name, "parenttype": "Sales Invoice", "parentfield": "sales_team"}, "sales_person")

            refund_amount1 = frappe.db.get_value("Sales Invoice", {"is_return": 1, "return_against": invoice_name}, 'base_grand_total') or 0
            refund_amount = frappe.db.sql("""
                SELECT SUM(grand_total) as grand_total , name as sales_invoice_refund
                FROM `tabSales Invoice`
                WHERE is_return = 1 AND return_against = %s
            """, invoice_name , as_dict=1)[0] or 0
            
            total_refund_amount += refund_amount.get('grand_total') or 0
            sales_invoice_refund = refund_amount.get('sales_invoice_refund')
            total_diff += diff
            total_net_total += net_total
            total_base_total_taxes_and_charges += base_total_taxes_and_charges
            total_grand_total += grand_total

            total_advance = 0
            
            mode_of_payment = None
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Sales Invoice"}, fields=["allocated_amount"])
            for entry in payment_entries:
                total_advance += entry.get("allocated_amount")
            total_advance_amount += total_advance
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Sales Invoice"}, fields=["parent"])
            total_amount_deduction = 0
            for entry in payment_entries:
                payment_entry = frappe.get_doc("Payment Entry", entry.get("parent"))
                mode_of_payment = payment_entry.mode_of_payment if payment_entry.mode_of_payment else None
                deductions = payment_entry.get('deductions')
                if deductions:
                    for i in deductions:
                        total_amount_deduction += i.amount 
                        print(total_amount_deduction)
            
            if idx == 0:
                customer_data.append({
                    "customer_name": customer_name,
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "set_warehouse": warehouse,
                    "status":status,
                    "net_total": net_total,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "sales_invoice_refund":sales_invoice_refund,
                    "refund_amount": refund_amount.get('grand_total') or 0,
                    "total_advance_amount": total_advance,
                    "total_amount_deduction":total_amount_deduction,
                    "diff": diff,
                    "sales_person": sales_person,
                    "mode_of_payment":mode_of_payment 
                })
            else:
                customer_data.append({
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "set_warehouse": warehouse,
                    "status":status,
                    "net_total": net_total,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "refund_amount": refund_amount.get('grand_total') or 0,
                    "sales_invoice_refund":sales_invoice_refund,
                    "total_advance_amount": total_advance,
                    "total_amount_deduction":total_amount_deduction,
                    "diff": diff,
                    "sales_person": sales_person ,
                    "mode_of_payment":mode_of_payment
                })

        data.extend(customer_data)
        if customer_data:
            data.append({
                "customer_name": "Totals Per Customer",
                "invoice_name": "",
                "posting_date": "",
                "set_warehouse": "",
                "net_total": total_net_total,
                "base_total_taxes_and_charges": total_base_total_taxes_and_charges,
                "grand_total": total_grand_total,
                "refund_amount": total_refund_amount,
                "sales_invoice_refund":sales_invoice_refund,
                "total_advance_amount": total_advance_amount,
                "total_amount_deduction":total_amount_deduction,
                "diff": total_diff
            })
    sum_half_net_totals = sum(customer.get("net_total", 0) / 2 for customer in data)
    total_net_total_all_customers = float(sum_half_net_totals)
    sum_half_base_total_taxes_and_charges = sum(customer.get("base_total_taxes_and_charges", 0) / 2 for customer in data)
    total_base_total_taxes_and_charges_all_customers = float(sum_half_base_total_taxes_and_charges)
    sum_half_grand_total = sum(customer.get("grand_total", 0) / 2 for customer in data)
    total_grand_total_all_customers = float(sum_half_grand_total)
    sum_half_refund_amount = sum(customer.get(refund_amount.get('grand_total' , 0) , 0) / 2 for customer in data)
    total_refund_amount_all_customers = float(sum_half_refund_amount)
    sum_half_total_advance_amount = sum(customer.get("total_advance_amount", 0) / 2 for customer in data)
    total_total_advance_amount_all_customers = float(sum_half_total_advance_amount)
    sum_half_diff = sum(customer.get("diff", 0) / 2 for customer in data)
    total_diff_all_customers = float(sum_half_diff)
    data.append({
        "customer_name": "Totals",
        "invoice_name": "",
        "posting_date": "",
        "set_warehouse": "",
        "net_total": total_net_total_all_customers,
        "base_total_taxes_and_charges": total_base_total_taxes_and_charges_all_customers,
        "grand_total":total_grand_total_all_customers ,
        "refund_amount": total_refund_amount_all_customers,
        "sales_invoice_refund":sales_invoice_refund,
        "total_advance_amount": total_total_advance_amount_all_customers,
        "total_amount_deduction":total_amount_deduction,
        "diff": total_diff_all_customers
    })

    if filters.get("value") and filters.get("operation"):
        if filters.get("operation") == '<':
            data = [entry for entry in data if 'diff' in entry and entry['diff'] < float(filters.get('value'))]
        if filters.get("operation") == '>':
            data = [entry for entry in data if 'diff' in entry and entry['diff'] > float(filters.get('value'))]
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
            "fieldname": "sales_invoice_refund",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "label":"Refund Invoice",
            "width": 200,
        },
        {
            "fieldname": "refund_amount",
            "fieldtype": "Currency",
            "label":"Refund",
            "width": 200,
        },
        {
            "fieldname": "total_amount_deduction",
            "fieldtype": "Currency",
            "label":"Deduction Amount",
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


        









