# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


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
    if filters.get("is_return") and filters.get("is_return") == 1:
        conditions.append(['name', 'in', frappe.db.sql_list("""
            SELECT DISTINCT return_against
            FROM `tabSales Invoice`
            WHERE is_return = 1
        """)])
          
    conditions.append(['status', 'not in', ['Draft', 'Cancelled','Return']])
    result = []
    sales_invoices = frappe.get_all("Sales Invoice", fields=["posting_date", "name", "set_warehouse", "customer",
                                                             "net_total", "base_total_taxes_and_charges",
                                                             "base_grand_total", "total_advance", "is_return", "return_against","outstanding_amount"],
                                    filters=conditions)

    for doc in sales_invoices:
        num = frappe.db.sql("""
            SELECT SUM(base_grand_total)
            FROM `tabSales Invoice`
            WHERE is_return = 1 AND return_against = %s
        """, doc.name)[0][0] or 0
        num2_values = frappe.db.sql_list("""
            SELECT name
            FROM `tabSales Invoice`
            WHERE is_return = 1 AND return_against = %s AND docstatus != 2  AND docstatus != 0
        """, doc.name)
        num2 = ', '.join(num2_values) if num2_values else ''
        total_advance = frappe.db.get_value("Payment Entry Reference",
                                             {"reference_name": doc.name, "reference_doctype": "Sales Invoice"},
                                             "allocated_amount") or 0
        temp = {}
        temp['posting_date'] = doc.posting_date
        temp['name'] = doc.name
        temp['warehouse'] = doc.set_warehouse
        temp['customer'] = doc.customer
        temp['net_total'] = doc.net_total
        temp['base_total_taxes_and_charges'] = doc.base_total_taxes_and_charges
        temp['base_grand_total'] = doc.base_grand_total
        temp['total_advance'] = total_advance
        temp['refund'] = num if num else 0
        temp['diff'] = doc.outstanding_amount
        temp['return_agent'] = num2
        
        result.append(temp)

    return result




def get_columns(filters):
	columns = [
		{
			"fieldname": "posting_date",
			"label": _("Date"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "name",
			"label": _("Serial"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200,
		},
        {
			"fieldname": "return_agent",
			"label": _("Return Agent"),
			"fieldtype": "Data",
			"width": 200,
		}, 
		{
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 200,
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200,
		},	
		{
			"fieldname": "net_total",
			"label": _("Total"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "base_total_taxes_and_charges",
			"label": _("Total Taxes And Charges"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "base_grand_total",
			"label": _("Grand Total"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "total_advance",
			"label": _("Total Allocated Amount"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "refund",
			"label": _("Refund"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "diff",
			"label": _("Differante"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns