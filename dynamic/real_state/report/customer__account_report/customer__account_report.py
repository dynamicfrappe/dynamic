# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	return CustomerAccountReport(filters).run()


class CustomerAccountReport(object):
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
						SELECT demo.* ,(demo.grand_total - demo.paid) as outstanding FROM (
						select `tabQuotation Item`.parent as quotation, `tabSales Order`.base_grand_total as grand_total,
						`tabSales Order Item`.parent as sales_order,`tabSales Invoice Item`.parent as sales_invoice
						,`tabSales Order Item`.item_code,`tabSales Order Item`.item_name
						,`tabSales Order Item`.uom,`tabItem`.item_group 
						,`tabSales Order`.payment_terms_template as payment_terms
						,(
						CASE 
						WHEN `tabSales Invoice Item`.parent is null and `tabSales Order Item`.parent is null  THEN 0.0
						WHEN `tabSales Order Item`.parent is not null and `tabSales Invoice Item`.parent is  null
						THEN (SELECT SUM(`tabPayment Entry Reference`.allocated_amount) FROM `tabPayment Entry Reference`
						WHERE `tabPayment Entry Reference`.reference_name=`tabSales Order Item`.parent 
						AND `tabPayment Entry Reference`.reference_doctype='Sales Order')
						WHEN `tabSales Order Item`.parent is not null and `tabSales Invoice Item`.parent is not null
						THEN (SELECT SUM(`tabPayment Entry Reference`.allocated_amount)  FROM `tabPayment Entry Reference`
						WHERE `tabPayment Entry Reference`.reference_name=`tabSales Invoice Item`.parent 
						AND `tabPayment Entry Reference`.reference_doctype='Sales Invoice')
						END
						) as paid
						FROM `tabQuotation Item`
						LEFT JOIN `tabItem`
						ON `tabQuotation Item`.item_code=`tabItem`.item_code
						LEFT JOIN  `tabQuotation`
						ON `tabQuotation Item`.parent=`tabQuotation`.name
						AND `tabQuotation Item`.item_code=`tabItem`.item_code
						LEFT JOIN `tabSales Order Item`
						ON `tabSales Order Item`.prevdoc_docname=`tabQuotation Item`.parent
						AND `tabSales Order Item`.item_code=`tabQuotation Item`.item_code 
						LEFT JOIN `tabSales Order`
						ON `tabSales Order`.name=`tabSales Order Item`.parent
						LEFT JOIN `tabSales Invoice Item`
						ON `tabSales Invoice Item`.sales_order=`tabSales Order Item`.parent 
						AND `tabSales Invoice Item`.item_code =`tabSales Order Item`.item_code 
						LEFT JOIN `tabSales Invoice`
						ON `tabSales Invoice`.name=`tabSales Invoice Item`.parent
						WHERE {conditions}
						)demo
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
				"width": 170,
			},
			{
				"label": _("Sales Order"),
				"fieldname": "sales_order",
				"fieldtype": "Link",
				"options": "Sales Order",
				"width": 170,
			},
			{
				"label": _("Sales Invoice"),
				"fieldname": "sales_invoice",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 170,
			},
			{
				"label": _("Paid"),
				"fieldname": "paid",
				"fieldtype": "Float",
				"width": 170,
			},
			{
				"label": _("Outstanding"),
				"fieldname": "outstanding",
				"fieldtype": "Float",
				"width": 170,
			},
			{
                "label": _("Item Group"),
                "fieldname": "item_group",
                "fieldtype": "Link",
				"options": "Item Group",
                "width": 180,
            },
	    {
                "label": _("Payemnet Terms Template"),
                "fieldname": "payment_terms",
                "fieldtype": "Link",
				"options": "Payemnet Terms Template",
                "width": 180,
            },
	    # {
        #         "label": _("Sales Invoice"),
        #         "fieldname": "sales_invoice",
        #         "fieldtype": "Link",
		# 		"options": "Sales Invoice",
        #         "width": 180,
        #     },
		# 	{
        #         "label": _("Status"),
        #         "fieldname": "status",
        #         "fieldtype": "Data",
        #         "width": 180,
        #     },
		]
		
