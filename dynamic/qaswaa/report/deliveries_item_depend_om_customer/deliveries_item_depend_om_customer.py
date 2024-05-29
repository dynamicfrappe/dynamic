# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = "1=1"
    
    if filters.get("customer_id"):
        conditions += f" AND se.customer_id = '{filters.get('customer_id')}'"
    if filters.get("sales_person"):
        conditions += f" AND st.sales_person = '{filters.get('sales_person')}'"
    
    sql_query = f"""
        SELECT 
            se.posting_date, 
            se.name,
            sed.item_code, 
            sed.item_name,
            se.stock_entry_type IN (
                SELECT name FROM `tabStock Entry Type` WHERE material_type = 'Dispensing Simples'
            ) AS outgoing, 
            st.sales_person
        FROM 
            `tabStock Entry` AS se
        INNER JOIN 
            `tabStock Entry Detail` AS sed ON se.name = sed.parent
        LEFT JOIN 
            `tabSales Team` AS st ON se.name = st.parent
        WHERE 
            {conditions} 
            AND se.docstatus = 1
    """

    result = frappe.db.sql(sql_query, as_dict=True)
    return result




def get_columns(filters):
	columns = [
		{
			"fieldname": "posting_date",
			"label": _("Date"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "name",
			"label": _("Stock Entry"),
			"fieldtype": "Link",
			"options": "Stock Entry",
			"width": 200,
		},
        # {
		# 	"fieldname": "stock_entry_type",
		# 	"label": _("Stock Entry Type"),
		# 	"fieldtype": "Link",
		# 	"options": "Stock Entry Type",
		# 	"width": 200,
		# }, 
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 200,
		},
		{
			"fieldname": "item_code",
			"label": _("Item Code"),
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
			"fieldname": "outgoing",
			"label": _("Outgoing"),
			"fieldtype": "Float",
			"width": 200,
		},
		{
			"fieldname": "recovered",
			"label": _("Recovered"),
			"fieldtype": "Float",
			"width": 200,
		},
		{
			"fieldname": "residual",
			"label": _("Residual"),
			"fieldtype": "Float",
			"width": 200,
		},
		
	]
	return columns


