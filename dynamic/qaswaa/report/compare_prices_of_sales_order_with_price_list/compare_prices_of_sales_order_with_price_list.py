# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_date(filters)
	return columns, data

def get_date(filters):
    conditions = " 1=1 "
    if filters.get("customer"):
        conditions += f""" and so.customer = "{filters.get('customer')}" """
    if filters.get("sales_order"):
        conditions += f""" and so.name = "{filters.get('sales_order')}" """
    if filters.get("date"):
        conditions += f""" and so.transaction_date = date("{filters.get('date')}") """
    if filters.get("price_list"):
        conditions += f""" and so.selling_price_list = "{filters.get('price_list')}" """
    if filters.get("sales_person"):
        conditions += f""" and st.sales_person = "{filters.get('sales_person')}" """
    if filters.get("set_warehouse"):
        conditions += f""" and so.set_warehouse = "{filters.get('set_warehouse')}" """     

    sql_query = f"""
        SELECT 
            so.name AS sales_order_name,
            soi.item_code,
            soi.item_name,
            soi.qty,
            soi.rate AS sales_rate,
            (SELECT pii.rate 
             FROM `tabPurchase Invoice` pi
             INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
             WHERE pi.docstatus = 1
             ORDER BY pi.creation DESC
             LIMIT 1) AS purchase_rate,
            soi.qty * (SELECT pii.rate 
                       FROM `tabPurchase Invoice` pi
                       INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                       WHERE pi.docstatus = 1
                       ORDER BY pi.creation DESC
                       LIMIT 1) AS total_cost,
            soi.rate - (SELECT pii.rate 
                         FROM `tabPurchase Invoice` pi
                         INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                         WHERE pi.docstatus = 1
                         ORDER BY pi.creation DESC
                         LIMIT 1) AS difference,
            soi.qty * (soi.rate - (SELECT pii.rate 
                                   FROM `tabPurchase Invoice` pi
                                   INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                                   WHERE pi.docstatus = 1
                                   ORDER BY pi.creation DESC
                                   LIMIT 1)) AS total_difference,
            ((soi.rate - (SELECT pii.rate 
                           FROM `tabPurchase Invoice` pi
                           INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                           WHERE pi.docstatus = 1
                           ORDER BY pi.creation DESC
                           LIMIT 1)) / (SELECT pii.rate 
                                        FROM `tabPurchase Invoice` pi
                                        INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                                        WHERE pi.docstatus = 1
                                        ORDER BY pi.creation DESC
                                        LIMIT 1)) * 100 AS difference_percentage
        FROM 
            `tabSales Order` so
        INNER JOIN 
            `tabSales Order Item` soi ON so.name = soi.parent
        LEFT JOIN
            `tabSales Team` st ON so.name = st.parent
        WHERE {conditions}
        """
        
    result = frappe.db.sql(sql_query, as_dict=True)
    return result






def get_columns():
	return[
		{
			"fieldname": "sales_order_name",
			"label": _("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 200,
		},
		{
			"fieldname": "item_code",
			"label": _("Item code"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"fieldname": "qty",
			"label": _("Qty"),
			"fieldtype": "Data",
			"width": 50,
		},
		{
			"fieldname": "sales_rate",
			"label": "Sales Rate",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "purchase_rate",
			"label": "Rate for Price List",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "total_cost",
			"label": "Total Cost",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "difference",
			"label": "Difference",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
	    {
			"fieldname": "total_difference",
			"label": "Total Difference",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100,
		},
		{
			"fieldname": "difference_percentage",
			"label": _("Difference Percentage"),
			"fieldtype": "Percent",
			"width": 100,
		}
		# {
		# 	"fieldname": "sales_rate",
		# 	"label": "Sales Rate",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 100,
		# },
		# {
		# 	"fieldname": "total_sales",
		# 	"label": "Total Sales",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 100,
		# },
		# {
		# 	"fieldname": "differance",
		# 	"label": "Differance",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 100,
		# },
		# {
		# 	"fieldname": "total_difference",
		# 	"label": "Total Difference",
		# 	"fieldtype": "Currency",
		# 	"options": "currency",
		# 	"width": 100,
		# },
		# {
		# 	"fieldname": "differance_percentage",
		# 	"label": _("Differance Percentage"),
		# 	"fieldtype": "Data",
		# 	"width": 100,
		# }
	]



