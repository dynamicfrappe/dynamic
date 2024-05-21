# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_purcashe_invoice_return

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_data(filters):
	conditions = [
                ('posting_date', '>=', filters.get("period_start_date")),
                ('posting_date', '<=', filters.get("period_end_date")),
                ('is_return', '=', 0)
            ]

	if filters.get("supplier"):
		conditions.append(("supplier" , "=" , filters.get("supplier")))
	if filters.get("company") :
		conditions.append(("company" , "=" , filters.get("company")))
	if filters.get("cost_center") :
		conditions.append(("cost_center" , "=" , filters.get("cost_center")))
	if filters.get("warehouse") :
		conditions.append(("set_warehouse" , "=" , filters.get("warehouse")))
	
	resulte = []
	doc = frappe.get_list("Purchase Invoice" , filters = conditions )
	for i in doc:
		temp = frappe.get_doc("Purchase Invoice" , i.name)
		refund_doc = None
		refund_name = get_purcashe_invoice_return(i.name)
		
		if refund_name:
			refund_doc = frappe.get_doc("Purchase Invoice" , refund_name)

		refund_doc_total = refund_doc.base_grand_total if refund_doc else 0

		temp1 = {
			'posting_date' : temp.posting_date,
			'name' : temp.name,
			'cost_center': temp.cost_center,
			'warehouse': temp.set_warehouse,
			'supplier': temp.supplier,
			'net_total': float(temp.net_total or 0) , 
			'base_total_taxes_and_charges' : float(temp.base_total_taxes_and_charges or 0),
			'base_grand_total': float(temp.base_grand_total or 0),
			'base_total_allocated_amount': float(temp.outstanding_amount or 0),
			'refund': refund_doc_total , 
			'unpaid': float(temp.base_grand_total or 0) - (abs(float(temp.outstanding_amount)) + abs(refund_doc_total) )
		}
		resulte.append(temp1)
	return resulte




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
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
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
			"fieldname": "base_total_allocated_amount",
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
			"fieldname": "Unpaid",
			"label": _("Unpaid"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns