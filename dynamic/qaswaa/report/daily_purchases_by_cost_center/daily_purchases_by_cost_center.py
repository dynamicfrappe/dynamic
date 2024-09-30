# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_purcashe_invoice_return

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_data(filters=None):
    result = []
    conditions = []

    if filters and filters.get("supplier"):
        conditions.append(['supplier', '=', filters.get("supplier")])
	if filters and filters.get("supplier_name"):
        conditions.append(['supplier_name', '=', filters.get("supplier_name")])
	if filters and filters.get("supplier_group"):
        suppliers_in_group = frappe.get_all("Supplier", filters={"supplier_group": filters.get("supplier_group")}, fields=["name"])
        supplier_names = [supplier.name for supplier in suppliers_in_group]
        if supplier_names:
            conditions.append(['supplier', 'in', supplier_names])
        else:
            return []
    if filters and filters.get("set_warehouse"):
        conditions.append(['set_warehouse', '=', filters.get("set_warehouse")])
    if filters and filters.get("cost_center"):
        conditions.append(['cost_center', '=', filters.get("cost_center")])        
    if filters and filters.get("period_start_date"):
        conditions.append(('posting_date', '>=', filters.get("period_start_date")))
    if filters and filters.get("period_end_date"):
        conditions.append(('posting_date', '<=', filters.get("period_end_date")))
    if filters and filters.get("is_return") and filters.get("is_return") == 1:
        conditions.append(['status', '=', 'Return'])
	if filters and filters.get("status"):
        conditions.append(['status', '=', filters.get("status") ])
    conditions.append(['docstatus', '!=', 2])

    purchases_invoices = frappe.get_all("Purchase Invoice", fields=["posting_date", "name", "set_warehouse", "supplier", "status",
                                                                    "net_total", "base_total_taxes_and_charges",
                                                                    "base_grand_total", "total_advance", "is_return", "return_against",
                                                                    "outstanding_amount"],
                                        filters=conditions)

    for doc in purchases_invoices:
        num = frappe.db.get_value("Purchase Invoice", {"is_return": 1, "return_against": doc.name}, 'base_grand_total') or 0

        total_advance = frappe.db.get_value("Payment Entry Reference",
                                             {"reference_name": doc.name, "reference_doctype": "Purchase Invoice"},
                                             "allocated_amount") or 0

        temp = {}
        temp['posting_date'] = doc.posting_date
        temp['name'] = doc.name
        temp['warehouse'] = doc.set_warehouse
        temp['supplier'] = doc.supplier
        temp['net_total'] = doc.net_total
        temp['base_total_taxes_and_charges'] = doc.base_total_taxes_and_charges
        temp['base_grand_total'] = doc.base_grand_total
        temp['total_advance'] = total_advance
        temp['refund'] = num if num else 0
        temp['unpaid'] = doc.outstanding_amount
        temp['return_agent'] = doc.return_against

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
			"options": "Purchase Invoice",
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
			"fieldname": "supplier",
			"label": _("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
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
			"fieldname": "unpaid",
			"label": _("Unpaid"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns