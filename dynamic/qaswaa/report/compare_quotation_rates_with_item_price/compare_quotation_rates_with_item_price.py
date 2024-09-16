# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters) , get_data(filters)
	return columns, data

def get_data(filters):
    conditions = "1=1"
    
    if filters.get("customer"):
        conditions += f" AND q.party_name = '{filters.get('customer')}'"
    if filters.get("quotation"):
        conditions += f" AND q.name = '{filters.get('quotation')}'"
    if filters.get("warehouse"):
        conditions += f" AND q.warehouse = '{filters.get('warehouse')}'"
    if filters.get("cost_center"):
        conditions += f" AND q.cost_center = '{filters.get('cost_center')}'"
    if filters.get("selling_price_list"):
        conditions += f" AND q.selling_price_list = '{filters.get('selling_price_list')}'"    
    if filters.get("from_date"):
        conditions += f" AND q.transaction_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND q.transaction_date <= '{filters.get('to_date')}'"

    data = frappe.db.sql(f"""
        SELECT
            q.name AS quotation,
			q.party_name,
			q.selling_price_list,
            qi.item_code AS item_code,
            qi.item_name AS item_name,
            qi.qty AS quantity,
            qi.net_rate AS rate,
            qi.base_price_list_rate AS price_of_price_list,
            (qi.qty * qi.base_price_list_rate) AS total_of_price_list,           
            (qi.qty * qi.net_rate) AS total_of_quotation,
            (qi.net_rate - qi.base_price_list_rate) AS diff,
            ((qi.qty * qi.base_price_list_rate) - (qi.qty * qi.net_rate)) AS total_diff,
            CASE WHEN (qi.qty * qi.base_price_list_rate) != 0
                 THEN ((qi.qty * qi.net_rate) - (qi.qty * qi.base_price_list_rate)) / (qi.qty * qi.base_price_list_rate)
                 ELSE 0
            END AS per_diff            
                         
        FROM
            `tabQuotation` q
        LEFT JOIN
            `tabQuotation Item` qi ON q.name = qi.parent
        WHERE
             {conditions}  AND q.docstatus != '2'
    """, as_dict=True)

    return data





def get_columns(filters):
	columns = [
		{
			"fieldname": "quotation",
			"label": _("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation",
			"width": 200,
		},
		{
			"fieldname": "party_name",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200,
		},
		{
			"fieldname": "selling_price_list",
			"label": _("Price List"),
			"fieldtype": "Link",
			"options": "Price List",
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
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "quantity",
			"label": _("Quantity"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "rate",
			"label": _("Price of Quotation"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 250,
		},
		{
			"fieldname": "price_of_price_list",
			"label": _("Price of Price List"),
			"fieldtype": "Data",
			"width": 100,
		},
        {
			"fieldname": "total_of_price_list",
			"label": _("Total of Price List"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "total_of_quotation",
			"label": _("Total of Quotation"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "diff",
			"label": _("Difference"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "total_diff",
			"label": _("Total Difference"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "per_diff",
			"label": _("Percentage Difference"),
			"fieldtype": "Percent",
			"width": 100,
		},
	]
	return columns
