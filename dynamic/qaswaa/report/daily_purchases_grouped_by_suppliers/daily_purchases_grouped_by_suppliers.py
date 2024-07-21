# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_data(filters):
	condition = " AND 1=1"

	if filters.get("supplier"):
		condition += f" and p.supplier = '{filters.get('supplier')}'"
	if filters.get("company") :
		condition += f" and p.company = '{filters.get('company')}'"
	sql =  f'''
		SELECT 
			p.supplier as supplier
		FROM 
			`tabPurchase Invoice` p
		WHERE 
			p.docstatus = 1
			AND p.posting_date >= '{filters.get('period_start_date')}'
			AND p.posting_date <= '{filters.get('period_end_date')}'
			{condition}
		GROUP BY 
			p.supplier ;
		'''
	suppliers = frappe.db.sql(sql , as_dict= 1)
	print(suppliers)

	resulte = []
	if suppliers:
		for i in suppliers:
			data = {}
			sums = {}
			data['supplier'] = i.supplier


			resulte.append(data)

			conditions = []
			if filters.get("cost_center"):
				conditions.append(('cost_center' , '=' , filters.get('cost_center')))
			if filters.get("warehouse") :
				conditions.append(('set_warehouse' , '=' , filters.get('warehouse')))

			
			conditions.append(("posting_date" , "<=" , filters.get("period_end_date")))
			conditions.append(("posting_date" , ">=" , filters.get("period_start_date")))
			conditions.append(('supplier', '=', i.supplier))
			conditions.append(('is_return', '=', 0))
			
			base_grand_total = 0
			net_total = 0
			base_total_taxes_and_charges = 0
			base_total_allocated_amount = 0
			refund = 0
			unpaid = 0
			refund_doc_total = 0

			temp = frappe.get_list(doctype = "Purchase Invoice" , filters = conditions , fields = ['posting_date' , 'name' , 'cost_center' , 'set_warehouse' , 'net_total' , 'base_total_taxes_and_charges' , 'base_grand_total' , 'outstanding_amount'])
			for j in temp:
				data1 = {}
				data1['posting_date'] = j.posting_date
				data1['name'] = j.name
				data1['cost_center'] = j.cost_center
				data1['warehouse'] = j.set_warehouse
				data1['net_total'] = j.net_total
				data1['base_total_taxes_and_charges'] = j.base_total_taxes_and_charges
				data1['base_grand_total'] = j.total



				
	
				data1['base_total_allocated_amount'] = j.outstanding_amount
				base_total_allocated_amount += j.outstanding_amount

				refund_name = get_purcashe_invoice_return(j.name)
				refund_doc = {
						'base_grand_total': 0,
					}
				if refund_name:
					refund_doc = frappe.get_doc("Purchase Invoice" , refund_name)

				
				if refund_doc:
					refund_doc_total = refund_doc.base_grand_total
					data1['refund'] = refund_doc_total
					
					refund += refund_doc_total
				data1['Unpaid'] =  float(j.total or 0) + (0 - float(j.outstanding_amount or 0)+ float(refund_doc_total or 0))
				unpaid += float(j.total or 0) + (0 - float(j.outstanding_amount or 0)+ float(refund_doc_total or 0))

				base_grand_total += j.total
				net_total += j.net_total
				base_total_taxes_and_charges += j.base_total_taxes_and_charges

				resulte.append(data1)

			sums['base_grand_total'] = base_grand_total 
			sums['net_total'] = net_total
			sums['base_total_taxes_and_charges'] = base_total_taxes_and_charges
			sums['base_total_allocated_amount'] = base_total_allocated_amount
			sums['refund'] = refund
			sums['unpaid'] = unpaid
			sums['warehouse'] = "Total"
			resulte.append(sums)


	return resulte

def get_purcashe_invoice_return(purchase_invoice):
	sql =  f'''
		SELECT 
			p.name as name
		FROM 
			`tabPurchase Invoice` p
		WHERE 
			p.is_return = 1
			AND p.return_against = '{purchase_invoice}';
		'''
	supplier = frappe.db.sql(sql , as_dict= 1)

	return supplier[0]['name'] if supplier else None

def get_columns(filters):
	columns = [
		{
			"fieldname": "supplier",
			"label": _("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 200,
		},
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
