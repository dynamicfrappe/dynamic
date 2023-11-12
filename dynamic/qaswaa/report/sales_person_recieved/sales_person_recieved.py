# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

# import frappe



import frappe
from frappe import _
from frappe.utils import  getdate
from frappe.utils import (
	flt,
)

def execute(filters=None):
	return sales_person_recieved(filters).run()


class sales_person_recieved(object):
	def __init__(self,filters):
		self.filters  = frappe._dict(filters or {})
	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_data(self):
		self.data = []
		self.data = self.get_transaction(self.filters)
		return self.data

	def get_transaction(self,filters):
		conditions = "  1=1 "
		data = self.get_new_opportunity(conditions)
		# frappe.errprint(f"all is ==> {get_new}")
		return data

	def get_new_opportunity(self,conditions):
		if self.filters.get("from_date"):
			conditions += " and `tabPayment Entry`.posting_date >= '%s'"%self.filters.get("from_date")
		if self.filters.get("to_date"):
			conditions += " and `tabPayment Entry`.posting_date <= '%s'"%self.filters.get("to_date")
		sql_query_new = f"""
			select `tabPayment Entry`.posting_date , `tabPayment Entry Reference`.reference_name  as sales_invoice 
			,`tabPayment Entry`.sales_person
			,sum(`tabPayment Entry Reference`.allocated_amount) as person_total_recieved
			,`tabPayment Entry Reference`.total_amount 
			FROM `tabPayment Entry`  
			inner join `tabPayment Entry Reference`
			ON `tabPayment Entry Reference`.parent=`tabPayment Entry`.name 
			where `tabPayment Entry Reference`.reference_doctype ='Sales Invoice'
			AND (`tabPayment Entry`.sales_person is not null and `tabPayment Entry`.sales_person != '')
			AND `tabPayment Entry`.docstatus=1
			AND {conditions}
			GROUP BY `tabPayment Entry Reference`.reference_name, `tabPayment Entry`.sales_person
		""".format(conditions=conditions)
		sql_data = frappe.db.sql(sql_query_new,as_dict=1)
		return sql_data



	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Sales Invoice"),
				"fieldname": "sales_invoice",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 250,
			},
			{
				"label": _("Sales Person"),
				"fieldname": "sales_person",
				"fieldtype": "Link",
				"options": "Sales Person",
				"width": 250,
			},
			{
				"label": _("Person Total Recieved"),
				"fieldname": "person_total_recieved",
				"fieldtype": "Float",
				"width": 250,
			},
			{
				"label": _("Invoice Amount"),
				"fieldname": "total_amount",
				"fieldtype": "Float",
				"width": 250,
			},
		]