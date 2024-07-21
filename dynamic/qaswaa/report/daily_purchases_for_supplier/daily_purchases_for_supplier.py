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
    suppliers = frappe.get_all("Supplier", fields=["name"])

    for supplier_idx, supplier in enumerate(suppliers):
        supplier_name = supplier.get("name")
        purchase_invoices_filters = {
            "supplier": supplier_name,
            "docstatus": ["!=", 2],
            "is_return": 0
        }
        
        if filters.get("cost_center"):
           purchase_invoices_filters['cost_center'] = [ "=", filters.get("cost_center")]  
        if filters.get("supplier_name"):
           purchase_invoices_filters['supplier_name'] = [ "=", filters.get("supplier_name")]       
        if filters.get("start_date") and filters.get("end_date"):
            purchase_invoices_filters["posting_date"] = ["between", [filters.get("start_date"), filters.get("end_date")]]
        elif filters.get("start_date") and not filters.get("end_date"):
            purchase_invoices_filters["posting_date"] = [">=", filters.get("start_date")]
        elif filters.get("end_date") and not filters.get("start_date"):
            purchase_invoices_filters["posting_date"] = ["<=", filters.get("end_date")]
        if filters.get("status"):
           status = filters.get("status")
           purchase_invoices_filters['status'] = ['in', status]                    
        

        purchase_invoices = frappe.get_all("Purchase Invoice", filters=purchase_invoices_filters, fields=["name", "posting_date", "net_total", "base_total_taxes_and_charges", "grand_total"])
        supplier_data = []
        total_refund_amount = 0
        total_advance_amount = 0 

        for idx, invoice in enumerate(purchase_invoices):
            invoice_name = invoice.get("name")
            posting_date = invoice.get("posting_date")
            net_total = invoice.get("net_total")
            base_total_taxes_and_charges = invoice.get("base_total_taxes_and_charges")
            grand_total = invoice.get("grand_total")

            refund_amount = frappe.db.get_value("Purchase Invoice", {"is_return": 1, "return_against": invoice_name}, 'base_grand_total') or 0
            total_refund_amount += refund_amount

            total_advance = 0
            payment_entries = frappe.get_all("Payment Entry Reference", filters={"reference_name": invoice_name, "reference_doctype": "Purchase Invoice"}, fields=["allocated_amount"])
            for entry in payment_entries:
                total_advance += entry.get("allocated_amount")
            total_advance_amount += total_advance

            diff = grand_total - total_advance + refund_amount
            
            if idx == 0:
                supplier_data.append({
                    "supplier_name": supplier_name,
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "net_total": net_total,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "refund_amount": refund_amount,
                    "total_advance_amount": total_advance,
                    "diff": diff,
                    
                })
            else:
                supplier_data.append({
                    "invoice_name": invoice_name,
                    "posting_date": posting_date,
                    "net_total": net_total,
                    "base_total_taxes_and_charges": base_total_taxes_and_charges,
                    "grand_total": grand_total,
                    "refund_amount": refund_amount,
                    "total_advance_amount": total_advance,
                    "diff": diff,
                })

        data.extend(supplier_data)
        if supplier_data:
            total_grand_total = sum([invoice.get("grand_total") for invoice in purchase_invoices])
            total_base_total_taxes_and_charges = sum([invoice.get("base_total_taxes_and_charges") for invoice in purchase_invoices])
            total_net_total = sum([invoice.get("net_total") for invoice in purchase_invoices])
            data.append({
                "supplier_name": "",
                "invoice_name": "",
                "posting_date": "",
                "net_total": total_net_total,
                "base_total_taxes_and_charges": total_base_total_taxes_and_charges,
                "grand_total": total_grand_total,
                "refund_amount": total_refund_amount,
                "total_advance_amount": total_advance_amount,
                "diff": total_grand_total - total_advance_amount + total_refund_amount
            })

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
        # {
        #     "label": "Warehouse", 
        #     "fieldname": "set_warehouse", 
        #     "fieldtype": "Link", 
        #     "options": "Warehouse"
        # },
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



        

     









