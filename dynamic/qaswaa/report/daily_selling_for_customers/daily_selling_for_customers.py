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
    conditions = []

    if filters.get("start_date"):
        conditions.append(['posting_date', '>=', filters.get("start_date")])
    if filters.get("end_date"):
        conditions.append(['posting_date', '<=', filters.get("end_date")])
    if filters.get("cost_center"):
        conditions.append(['cost_center', '=', filters.get("cost_center")])
    if filters.get("warehouse"):
        conditions.append(['warehouse', '=', filters.get("warehouse")])
    if filters.get("customer"):
        conditions.append(['customer', '=', filters.get("customer")])
    if filters.get("sales_person"):
        conditions.append(['sales_person', '=', filters.get("sales_person")])
    if filters.get("sales_partner"):
        conditions.append(['sales_partner', '=', filters.get("sales_partner")])    
                   
    result = []
    sales_invoices = frappe.get_all("Sales Invoice", fields=["posting_date", "name", "set_warehouse", "customer",
                                                             "net_total", "base_total_taxes_and_charges",
                                                             "base_grand_total", "total_advance"], filters=conditions)

    for doc in sales_invoices:
        num = frappe.db.get_value("Sales Invoice", {"is_return": 1, "return_against": doc.name}, 'base_grand_total') or 0
        
        total_advance = frappe.db.get_value("Payment Entry Reference",
                                             {"reference_name": doc.name, "reference_doctype": "Sales Invoice"},
                                             "allocated_amount") or 0
        
        temp = {}
        temp['customer'] = doc.customer
        temp['sales_person'] = get_sales_person(doc.name)  
        result.append(temp)

        temp_details = {}
        temp_details['posting_date'] = doc.posting_date
        temp_details['name'] = doc.name
        temp_details['warehouse'] = doc.set_warehouse
        temp_details['net_total'] = doc.net_total
        temp_details['base_total_taxes_and_charges'] = doc.base_total_taxes_and_charges
        temp_details['base_grand_total'] = doc.base_grand_total
        temp_details['total_advance'] = total_advance
        temp_details['refund'] = num if num else 0
        temp_details['diff'] = float(total_advance) + (float(num or 0))
        
        result.append(temp_details)
        result.append({})

    return result

def get_sales_person(sales_invoice_name):
    sales_team = frappe.get_all("Sales Team", filters={"parent": sales_invoice_name}, fields=["sales_person"])
    if sales_team:
        return sales_team[0].get("sales_person")
    else:
        return None




def get_columns(filters):
    columns_customer = [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200,
        },
        {
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 200,
        },
    ]

    columns_details = [
        {
            "fieldname": "posting_date",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 200,
        },
        {
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 200,
        },
        {
            "fieldname": "net_total",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "base_total_taxes_and_charges",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "base_grand_total",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "total_advance",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "refund",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "diff",
            "fieldtype": "Data",
            "width": 200,
        },
    ]

    # Concatenate columns
    columns = columns_customer + columns_details[1:]
    return columns


