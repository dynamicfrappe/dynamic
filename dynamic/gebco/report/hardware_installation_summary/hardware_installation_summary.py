# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	return instalation_summary(filters).run()


class instalation_summary(object):
	def __init__(self,filters=None):
		self.filters = frappe._dict(filters or {})
	
	def run(self):
		self.get_columns()
		self.get_data()
		return self.columns, self.data

	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Doctype",
				"width": 130,
			},
            {
                "fieldname": "sales_order",
                "fieldtype": "Link",
                "label": _("Sales Order"),
                "width": 120,
                "options": "Sales Order",
            },
			{
                "fieldname": "total_cars",
                "fieldtype": "Int",
                "label": _("Total Car"),
                "width": 120,
            },
			{
                "fieldname": "requested_car",
                "fieldtype": "Int",
                "label": _("requested Car"),
                "width": 120,
            },
			{
                "fieldname": "ordered_car",
                "fieldtype": "Int",
                "label": _("Ordered Car"),
                "width": 120,
            },
			{
                "fieldname": "completed_car",
                "fieldtype": "Int",
                "label": _("Completed Car"),
                "width": 120,
            },
			
        ]
		return self.columns
		
	
	def get_data(self):
		self.data = []
		self.conditions, self.values,self.query = self.get_conditions(self.filters)

		data = f"""{self.query} where {self.conditions}
				
				"""

		self.data = frappe.db.sql(data, values=self.values, as_dict=1)
		
		frappe.errprint(f'data-->{self.data}')
		return self.data

		
	def get_conditions(self,filters):
		conditions = "1=1 "
		values = dict()
		query = ""
		dict_fields = {
			"Installation Request":['p.sales_order',"p.customer","p.total_cars","p.completed_cars as `completed_car`"," p.ordered_cars as `ordered_car`"],
			"Installation Order":['p.sales_order','p.customer','p.total_cars'],
			"Sales Order":[]
		}
		#TODO: convert to one query AND show all data from sales Order if Not select on of source
		if self.filters.get('source'):
			if self.filters.get('source') == "Installation Request":
				query_fields = self.get_query_field(dict_fields["Installation Request"])
				query = f"Select {query_fields} `tabInstallation Request` p  "
				conditions += " AND p.name  =  %(doc_name)s "
				values["doc_name"] = filters.get("doc_name")

			if self.filters.get('source') == "Installation Order":
				query_fields = self.get_query_field(dict_fields["Installation Order"])
				query = "Select  {query_fields} from `tabInstallation Order` p  "
				conditions += " AND p.name  =  %(doc_name)s "
				values["doc_name"] = filters.get("doc_name")

			if self.filters.get('source') == "Sales Order":
				query = "select p.name as `sales_order`, sum(p.total_cars) as total_cars,sum(re.total_cars) as requested_car from `tabSales Order` as p,`tabInstallation Request` as re"
				conditions += " AND p.name  =  %(doc_name)s "
				values["doc_name"] = filters.get("doc_name")

		return conditions, values, query
		
	def get_query_field(self,list_field):
		fields = ''
		for field in list_field:
			fields += field + ' ,'
		frappe.errprint(fields[:-1])
		return fields[:-1]


# requested_cars_result = frappe.db.sql(f"""
# 		select sum(total_cars) as total_cars from `tabInstallation Request` 
# 		where docstatus = 1 and  sales_order = '{sales_order.name}'
# 	""",as_dict=1) or 0
# 	total_order_result = frappe.db.sql(f"""
# 		select sum(total_cars) as total_cars from `tabInstallation Order` 
# 		where docstatus = 1 and  sales_order = '{sales_order.name}'
# 	""",as_dict=1) or 0
# 	completed_qty_result = frappe.db.sql(f"""
# 		select sum(1) as completed_qty from `tabCar Installation` 
# 		where docstatus = 1 and  sales_order = '{sales_order.name}'
# 	""",as_dict=1) or 0