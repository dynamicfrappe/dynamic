# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_purcashe_invoice_return

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_data(filters=None):
    conditions = [('is_return', '=', 0)]
    
    if filters and filters.get("period_start_date"):
        conditions.append(('posting_date', '>=', filters.get("period_start_date")))
    if filters and filters.get("period_end_date"):
        conditions.append(('posting_date', '<=', filters.get("period_end_date")))

    result = []
    purchase_invoices = frappe.get_list("Purchase Invoice", filters=conditions)
    
    for invoice in purchase_invoices:
        temp = frappe.get_doc("Purchase Invoice", invoice.name)
        refund_doc = None
        refund_name = get_purcashe_invoice_return(invoice.name)
        
        if refund_name:
            refund_doc = frappe.get_doc("Purchase Invoice", refund_name)

        refund_doc_total = refund_doc.base_grand_total if refund_doc else 0
        
        allocated_amount = 0
        payment_references = frappe.get_all("Payment Entry Reference",
                                             filters={"reference_doctype": "Purchase Invoice",
                                                      "reference_name": invoice.name},
                                             fields=["allocated_amount"])
        for reference in payment_references:
            allocated_amount += reference.allocated_amount
        
        temp1 = {
            'posting_date': temp.posting_date,
            'name': temp.name,
            'cost_center': temp.cost_center,
            'warehouse': temp.set_warehouse,
            'supplier': temp.supplier,
            'net_total': float(temp.net_total or 0),
            'base_total_taxes_and_charges': float(temp.base_total_taxes_and_charges or 0),
            'base_grand_total': float(temp.base_grand_total or 0),
            'base_total_allocated_amount': allocated_amount,
            'refund': refund_doc_total,
            'unpaid': float(temp.base_grand_total or 0) - abs(float(temp.outstanding_amount))
        }
        result.append(temp1)
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
			"fieldname": "unpaid",
			"label": _("Unpaid"),
			"fieldtype": "Data",
			"width": 200,
		},
	]
	return columns