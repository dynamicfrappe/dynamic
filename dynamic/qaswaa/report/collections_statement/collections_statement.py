# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters) :
	conditions = " 1=1"
	if filters.get("from_date"):
		conditions += f" and pe.posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		conditions += f" and pe.posting_date <= '{filters.get('to_date')}'"
	sql = f"""select  pe.name , pe.posting_date , pe.total_allocated_amount , pe.reference_date ,
	    per.bill_no , per.reference_name ,  per.due_date , per.total_amount , per.allocated_amount
		FROM `tabPayment Entry` pe
		inner join `tabPayment Entry Reference` per 
		on pe.name = per.parent 
		where pe.docstatus = 1 and {conditions}
		"""
	results = frappe.db.sql(sql,as_dict=1)

	data = []
	repated_name = []
	for result in results :
		dict = {}
		if result["name"] not in repated_name :
			repated_name.append(result["name"])
			dict["name"] = result["name"]
		dict["posting_date"] = result["posting_date"]
		dict["total_allocated_amount"] = result["total_allocated_amount"]
		dict["reference_date"] = result["reference_date"]
		dict["bill_no"] = result["bill_no"]
		dict["reference_name"] = result["reference_name"]
		dict["due_date"] = result["due_date"]
		dict["total_amount"] = result["total_amount"]
		dict["allocated_amount"] = result["allocated_amount"]
		data.append(dict)
	
	return data

def get_columns():
	columns = [
			{
				"label": _("Payment Entry"),
				"fieldname": "name",
				"fieldtype": "Link",
				"options": "Payment Entry",
				"width": 150,
			},
			{
				"label": _("Posting Date"),
				"fieldname": "posting_date",
				"fieldtype": "Date",
				"width": 150,
			},
			{
				"label": _("Total Allocated Amount"),
				"fieldname": "total_allocated_amount",
				"fieldtype": "Float",
				"width": 150,
			},
			{
				"label": _("Cheque/Reference Date"),
				"fieldname": "reference_date",
				"fieldtype": "Date",
				"width": 150,
			},
			{
				"label": _("Invoice Amount"),
				"fieldname": "total_amount",
				"fieldtype": "Float",
				"width": 150,
			},
			{
				"label": _("Supplier Invoice No"),
				"fieldname": "bill_no",
				"fieldtype": "Data",
				"width": 150,
			},
			{
				"label": _("Sales Invoice"),
				"fieldname": "reference_name",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 150,
			},
			{
				"label": _("Due Date"),
				"fieldname": "due_date",
				"fieldtype": "Date",
				"width": 150,
			},
			{
				"label": _("Grand Total"),
				"fieldname": "total_amount",
				"fieldtype": "Float",
				"width": 150,
			},
			{
				"label": _("Allocated"),
				"fieldname": "allocated_amount",
				"fieldtype": "Float",
				"width": 150,
			},
		]
	return columns