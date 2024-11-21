# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

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
    suppliers = frappe.get_all("Supplier", fields=["name"])

    for supplier_idx, supplier in enumerate(suppliers):
        supplier_name = supplier.get("name")
        purchase_invoices_filters = {
            "supplier": supplier_name,
            "docstatus": ["!=", 2],
            "is_return": 0,
        }
        
        if filters.get("cost_center"):
            purchase_invoices_filters['cost_center'] = ["=", filters.get("cost_center")]
        if filters.get("supplier_name"):
            purchase_invoices_filters['supplier_name'] = ["=", filters.get("supplier_name")]
        if filters.get("set_warehouse"):
            purchase_invoices_filters['set_warehouse'] = ["=", filters.get("set_warehouse")]   
                 
        if filters.get("start_date") and filters.get("end_date"):
            purchase_invoices_filters["posting_date"] = ["between", [filters.get("start_date"), filters.get("end_date")]]
        elif filters.get("start_date") and not filters.get("end_date"):
            purchase_invoices_filters["posting_date"] = [">=", filters.get("start_date")]
        elif filters.get("end_date") and not filters.get("start_date"):
            purchase_invoices_filters["posting_date"] = ["<=", filters.get("end_date")]
        if filters.get("status"):
            status = filters.get("status")
            purchase_invoices_filters['status'] = ['in', status]
        purchase_invoices_filters['status'] = ['not in', ['Draft', 'Cancelled']]                      
        
        sales_invoices = frappe.get_all("Purchase Invoice", filters=purchase_invoices_filters, fields=["name", "posting_date", "set_warehouse", "net_total", "base_total_taxes_and_charges", "grand_total", "outstanding_amount","status"])
        
        supplier_data = []
        total_refund_amount = 0
        total_advance_amount = 0
        total_diff = 0
        temp = 0
        total_net_total = 0
        total_base_total_taxes_and_charges = 0
        total_grand_total = 0
        purchase_invoice_refund = ''
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

            refund_amount1 = frappe.db.get_value("Purchase Invoice", {"is_return": 1, "return_against": invoice_name}, 'base_grand_total') or 0
            refund_amount = frappe.db.sql("""
                SELECT SUM(grand_total) as grand_total , name as purchase_invoice_refund
                FROM `tabPurchase Invoice`
                WHERE is_return = 1 AND return_against = %s
            """, invoice_name , as_dict=1)[0] or 0
            
            total_refund_amount += refund_amount.get('grand_total') or 0
            purchase_invoice_refund = refund_amount.get('purchase_invoice_refund')
            total_diff += diff
            total_net_total += net_total
            total_base_total_taxes_and_charges += base_total_taxes_and_charges
            total_grand_total += grand_total

            total_advance = 0
            
            mode_of_payment = None
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Purchase Invoice"}, fields=["allocated_amount"])
            for entry in payment_entries:
                total_advance += entry.get("allocated_amount")
            total_advance_amount += total_advance
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Purchase Invoice"}, fields=["parent"])
            total_amount_deduction = 0
            for entry in payment_entries:
                payment_entry = frappe.get_doc("Payment Entry", entry.get("parent"))
                mode_of_payment = payment_entry.mode_of_payment if payment_entry.mode_of_payment else None
                # deductions = payment_entry.get('deductions')
                # if deductions:
                #     for i in deductions:
                #         total_amount_deduction += i.amount 
                #         print(total_amount_deduction)
           
            against_pi = invoice_name
            gl_entries = frappe.db.sql(
                    f"""
                    select voucher_no
                    from `tabGL Entry`
                    where voucher_type = 'Journal Entry' AND against_voucher = '{against_pi}' """, as_dict=1 )
            print(gl_entries)
            for gl_entry in gl_entries:
                je = frappe.get_doc("Journal Entry", gl_entry.get('voucher_no'))
                credit = je.total_credit
                print(credit)
                total_amount_deduction += credit
            
            if idx == 0:
                supplier_data.append({
                    "supplier_name": supplier_name,
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "set_warehouse": warehouse,
                    "status":status,
                    "net_total": net_total,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "purchase_invoice_refund":purchase_invoice_refund,
                    "refund_amount": refund_amount.get('grand_total') or 0,
                    "total_advance_amount": total_advance,
                    "total_amount_deduction":total_amount_deduction,
                    "diff": diff,
                    "mode_of_payment":mode_of_payment 
                })
            else:
                supplier_data.append({
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "set_warehouse": warehouse,
                    "status":status,
                    "net_total": net_total,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "refund_amount": refund_amount.get('grand_total') or 0,
                    "purchase_invoice_refund":purchase_invoice_refund,
                    "total_advance_amount": total_advance,
                    "total_amount_deduction":total_amount_deduction,
                    "diff": diff,
                    "mode_of_payment":mode_of_payment
                })

        data.extend(supplier_data)
        if supplier_data:
            data.append({
                "supplier_name": "Totals Per Supplier",
                "invoice_name": "",
                "posting_date": "",
                "set_warehouse": "",
                "net_total": total_net_total,
                "base_total_taxes_and_charges": total_base_total_taxes_and_charges,
                "grand_total": total_grand_total,
                "refund_amount": total_refund_amount,
                "purchase_invoice_refund":purchase_invoice_refund,
                "total_advance_amount": total_advance_amount,
                "total_amount_deduction":total_amount_deduction,
                "diff": total_diff
            })
    # sum_half_net_totals = sum(supplier.get("net_total", 0) / 2 for Supplier in data)
    # sum_half_net_totals = next((row for row in data if row.get("supplier") == 'Totals Per Supplier' ))
    sum_half_net_totals = sum(
        supplier.get("net_total", 0)
        for supplier in data 
        if supplier.get("supplier_name") == "Totals Per Supplier"
    )

    total_net_total_all_suppliers = float(sum_half_net_totals)

    sum_half_base_total_taxes_and_charges = sum(supplier.get("base_total_taxes_and_charges", 0) / 2 for supplier in data)
    total_base_total_taxes_and_charges_all_suppliers = float(sum_half_base_total_taxes_and_charges)

    sum_half_grand_total = sum(supplier.get("grand_total", 0) / 2 for supplier in data)
    total_grand_total_all_suppliers = float(sum_half_grand_total)
    
    sum_half_refund_amount = sum(supplier.get(refund_amount.get('grand_total' , 0) , 0) / 2 for supplier in data)
    total_refund_amount_all_suppliers = float(sum_half_refund_amount)
    
    sum_half_total_advance_amount = sum(supplier.get("total_advance_amount", 0) / 2 for supplier in data)
    total_total_advance_amount_all_suppliers = float(sum_half_total_advance_amount)
    
    sum_half_diff = sum(supplier.get("diff", 0) / 2 for supplier in data)
    total_diff_all_suppliers = float(sum_half_diff)
    
    data.append({
        "supplier_name": "Totals",
        "invoice_name": "",
        "posting_date": "",
        "set_warehouse": "",
        "net_total": total_net_total_all_suppliers,
        "base_total_taxes_and_charges": total_base_total_taxes_and_charges_all_suppliers,
        "grand_total":total_grand_total_all_suppliers ,
        "refund_amount": total_refund_amount_all_suppliers,
        "purchase_invoice_refund":purchase_invoice_refund,
        "total_advance_amount": total_total_advance_amount_all_suppliers,
        "total_amount_deduction":total_amount_deduction,
        "diff": total_diff_all_suppliers
    })

    if filters.get("value") and filters.get("operation"):
        if filters.get("operation") == '<':
            data = [entry for entry in data if 'diff' in entry and entry['diff'] < float(filters.get('value'))]
        if filters.get("operation") == '>':
            data = [entry for entry in data if 'diff' in entry and entry['diff'] > float(filters.get('value'))]
    print ("data =" ,data)
    return data



def get_columns(filters):
    
    columns = [
        {
            "label": "Supplier Name", 
            "fieldname": "supplier_name", 
            "fieldtype": "Link", 
            "options": "Supplier"
        },
        
        {
            "label": "Invoice Name", 
            "fieldname": "invoice_name", 
            "fieldtype": "Link", 
            "options": "Purchase Invoice"
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
            "label":"Status",
            "fieldname":"status",
            "fieldtype":"Select",
            "options": "\nDraft\nReturn\nDebit Note Issued\nSubmitted\nPaid\nPartly Paid\nUnpaid\nOverdue\nCancelled\nInternal Transfer"
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
            "fieldname": "purchase_invoice_refund",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
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