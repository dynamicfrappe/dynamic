# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters):

	condition = " AND 1=1"
	
	if filters.get("customer"):
		condition += f" and si.customer = '{filters.get('customer')}'"
	
	sql =  f'''
		SELECT 
			si.customer as customer,
			st.sales_person as sales_person
		FROM 
			`tabSales Invoice` si
		INNER JOIN
			`tabSales Team` st
		ON
			si.name = st.parent
		WHERE 
			si.docstatus = 1
			AND si.posting_date >= '{filters.get('period_start_date')}'
			AND si.posting_date <= '{filters.get('period_end_date')}'
			{condition}
		GROUP BY 
			si.customer,
			st.sales_person
		'''
	customers = frappe.db.sql(sql , as_dict= 1)

	results = []
	if customers:
		for i in customers:
			data = {}
			data['customer'] = i.customer
			results.append(data)

			conditions = [
				['posting_date', '>=', filters.get('period_start_date')],
				['posting_date', '<=', filters.get('period_end_date')]
			]
			if filters.get("customer"):
				conditions.append(['customer', '=', filters.get('customer')])

			temp = frappe.db.get_list("Sales Invoice", filters=conditions)
			print(temp)
			
			
			for j in temp:
				invoice = frappe.get_doc("Sales Invoice", j.name)
				items = invoice.get("items")
				
				if i.customer == invoice.customer:
					data2 = {
						'posting_date': invoice.posting_date,
						'name': invoice.name,
						'sales_person': i.sales_person
					}
					results.append(data2)
					
					for idx, z in enumerate(items):
						data1 = {
							'item_code': z.item_code,
							'item_name': z.item_name
						}
						
						doc_of_delivery = get_delivary(j.name)
						if doc_of_delivery:
							docs = frappe.get_doc("Delivery Note", doc_of_delivery)
							items_of_del = docs.get("items")
							
							if idx < len(items_of_del):
								delivered = items_of_del[idx].qty
								data1['deliverd'] = float(delivered or 0)
								
								doc_of_refund = get_returned(doc_of_delivery)
								if doc_of_refund:
									docss = frappe.get_doc("Delivery Note", doc_of_refund)
									items_of_refund = docss.get("items")
									
									if idx < len(items_of_refund):
										refund = items_of_refund[idx].qty
										data1['refund'] = float(refund or 0)
										data1['differante'] = float(data1['deliverd'] or 0) + float(refund or 0)
						
						results.append(data1)



	return results
		

def get_columns(filters):
	columns = [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
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
			"options": "Sales Invoice",
			"width": 200,
		},
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "item_code",
			"label": _("Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 200,
		},
		{
			"fieldname": "item_name",
			"label": _("Item"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "deliverd",
			"label": _("Deliverd"),
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
			"fieldname": "differante",
			"label": _("Differante"),
			"fieldtype": "Data",
			"width": 200,
		},
		
	]
	return columns


@frappe.whitelist()
def get_delivary(sales_invoice):
	sql =  f'''
		SELECT 
			d.name as name 
		FROM 
			`tabDelivery Note` d
		JOIN
			`tabDelivery Note Item` dt
		ON
			d.name = dt.parent
		WHERE 
			d.docstatus = 1 
			AND d.is_return = 0
			AND dt.against_sales_invoice = '{sales_invoice}'
		'''
	
	doc = frappe.db.sql(sql , as_dict= 1)
	if doc:
		return doc[0]['name']
	else:
		return False

@frappe.whitelist()
def get_returned(delivery_note):
	sql =  f'''
		SELECT 
			d.name as name
		FROM 
			`tabDelivery Note` d
		WHERE 
			d.docstatus = 1 
			AND d.is_return = 1
			AND d.return_against = '{delivery_note}'
		'''
	doc = frappe.db.sql(sql , as_dict= 1)
	return doc[0]['name'] if doc else None