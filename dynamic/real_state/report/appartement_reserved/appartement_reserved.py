# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	return AppartementReserved(filters).run()


class AppartementReserved(object):
	def __init__(self,filters):
		self.filters  = frappe._dict(filters or {})
		
	def run(self):
		# self.data = []
		self.get_columns()
		self.data = self.get_data()
		return self.columns, self.data

	def get_data(self):
		self.data = []
		self.data = self.get_transaction(self.filters)
		# self.data = self.get_data()
		return self.data

	def get_transaction(self,filters):
		get_new = self.get_data()
		# frappe.errprint(f"all is ==> {get_new}")
		return get_new

	def get_data(self):
		conditions = "  1=1 "
		# if self.filters.get("from_date"):
		# 	conditions += " and `tabReservation`.creation >= '%s'"%self.filters.get("from_date")
		# if self.filters.get("to_date"):
		# 	conditions += " and `tabReservation`.creation <= '%s'"%self.filters.get("to_date")
		if self.filters.get("item_code"):
			conditions += " and `tabItem`.item_code = '%s'"%self.filters.get("item_code")
		# if self.filters.get("cost_center"):
		# 	conditions += " and so.cost_center = '%s'"%self.filters.get("cost_center")
		
			
		sql_query_new = f"""
						select `tabItem`.item_code,`tabItem`.item_name,`tabQuotation Item`.parent as quotation,
						`tabSales Order Item`.parent as sales_order,`tabSales Invoice Item`.parent as sales_invoice
						,(
						CASE 
						WHEN `tabSales Invoice Item`.parent is null and `tabQuotation Item`.parent is null  THEN 'Exist'
						WHEN `tabSales Invoice Item`.parent is null and `tabQuotation Item`.parent is not null  THEN 'Reserved'
						WHEN `tabSales Invoice Item`.parent is not null  THEN 'Sold'
						END
						) as status
						FROM `tabItem`
						LEFT JOIN `tabQuotation Item`
						ON `tabQuotation Item`.item_code=`tabItem`.item_code
						LEFT JOIN `tabSales Order Item`
						ON `tabSales Order Item`.prevdoc_docname=`tabQuotation Item`.parent
						AND `tabSales Order Item`.item_code=`tabQuotation Item`.item_code 
						LEFT JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.sales_order=`tabSales Order Item`.parent 
						AND `tabSales Invoice Item`.item_code =`tabSales Order Item`.item_code 
						WHERE {conditions} 
						ORDER BY `tabQuotation Item`.parent DESC limit 20
		""".format(conditions=conditions)
		sql_data = frappe.db.sql(sql_query_new,as_dict=1)
		# frappe.errprint(f"sql_data ==> {sql_data}")
		return sql_data

	def get_columns(self):
		# add columns wich appear data
		self.columns = [
			{
				"label": _("Item Name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 180,
			},
			{
				"label": _("Item"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 170,
			},
			{
                "label": _("Quotation"),
                "fieldname": "quotation",
                "fieldtype": "Link",
				"options": "Quotation",
                "width": 180,
            },
	    {
                "label": _("Sales Order"),
                "fieldname": "sales_order",
                "fieldtype": "Link",
				"options": "Sales Order",
                "width": 180,
            },
	    {
                "label": _("Sales Invoice"),
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
				"options": "Sales Invoice",
                "width": 180,
            },
			{
                "label": _("Status"),
                "fieldname": "status",
                "fieldtype": "Data",
                "width": 180,
            },
		]
		
