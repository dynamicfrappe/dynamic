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
                "fieldname": "from_time",
                "fieldtype": "Date",
                "label": _("From"),
                "width": 150
            },
            {
                "fieldname": "to_time",
                "fieldtype": "Date",
                "label": _("To"),
                "width": 150
            },
            {
                "fieldname": "sales_order",
                "fieldtype": "Link",
                "label": _("Sales Order"),
                "width": 120,
                "options": "Sales Order",


            },
            {
                "fieldname": "installation_order",
                "fieldtype": "Link",
                "label": _("Installation Order"),
                "width": 120,
                "options": "Installation Order",
            },
            {
                "fieldname": "installation_request",
                "fieldtype": "Link",
                "label": _("Installation Request"),
                "width": 120,
                "options": "Installation Request",
            },
            {
                "fieldname": "team",
                "fieldtype": "Link",
                "label": _("Installation Team"),
                "width": 120,
                "options": "Installation Team",
            },
			{
                "fieldname": "requested_car",
                "fieldtype": "Int",
                "label": _("requested Car"),
                "width": 70,
            },
			{
                "fieldname": "ordered_car",
                "fieldtype": "Int",
                "label": _("Ordered Car"),
                "width": 70,
            },
			{
                "fieldname": "completed_car",
                "fieldtype": "Int",
                "label": _("Completed Car"),
                "width": 70,
            },
        ]
		return self.columns
		
	
	def get_data(self):
		self.data = []
		self.conditions, self.values = self.get_conditions(self.filters)
		query = ''
		# data_query = f"""
		# 	select * {query}
		# 	from `tabInstallation Request` p
		# 	where {self.conditions}
			
		# """
		return self.data
	
	def get_conditions(self,filters):
		conditions = "1=1 "
		values = dict()

		if filters.get('sales_order'):
			conditions += " AND p.sales_order  =  %(sales_order)s "
			values["sales_order"] = filters.get("sales_order")

		if filters.get('installation_order'):
			conditions += " AND p.installation_order  =  %(installation_order)s "
			values["installation_order"] = filters.get("installation_order")

		if filters.get('installation_request'):
			conditions += " AND p.installation_request  =  %(installation_request)s "
			values["installation_request"] = filters.get(
				"installation_request")

