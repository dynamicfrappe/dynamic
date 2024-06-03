# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = "1=1"
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if from_date:
        conditions += f""" AND se.posting_date >= date('{from_date}')"""
    if to_date:
        conditions += f""" AND se.posting_date <= date('{to_date}')"""
    if filters.get("customer_id"):
        conditions += f""" AND se.customer_id = '{filters.get('customer_id')}'"""
    if filters.get("sales_person"):
        conditions += f""" AND st.sales_person = '{filters.get('sales_person')}'"""

    sql_query = f"""
        SELECT 
            se.posting_date,
            se.name, 
            sed.item_code, 
            sed.item_name, 
            st.sales_person,
            CASE 
                WHEN se.stock_entry_type = (
                    SELECT name 
                    FROM `tabStock Entry Type` 
                    WHERE matrial_type = 'Dispensing Simples'
                ) THEN sed.qty
                ELSE NULL
            END AS outgoing,
            (
                SELECT SUM(sed_inner.qty)
                FROM `tabStock Entry` AS se_inner 
                INNER JOIN `tabStock Entry Detail` AS sed_inner 
                    ON se_inner.name = sed_inner.parent 
                WHERE se.name = se_inner.old_stock_entry 
                AND sed_inner.item_code = sed.item_code
            ) AS recovered,
            CASE 
                WHEN se.stock_entry_type = (
                    SELECT name 
                    FROM `tabStock Entry Type` 
                    WHERE matrial_type = 'Dispensing Simples'
                ) THEN 
                    sed.qty - COALESCE(
                        (
                            SELECT SUM(sed_inner.qty)
                            FROM `tabStock Entry` AS se_inner 
                            INNER JOIN `tabStock Entry Detail` AS sed_inner 
                                ON se_inner.name = sed_inner.parent 
                            WHERE se.name = se_inner.old_stock_entry 
                            AND sed_inner.item_code = sed.item_code
                        ), 0)
                ELSE NULL
            END AS residual
        FROM 
            `tabStock Entry` AS se
        INNER JOIN 
            `tabStock Entry Detail` AS sed ON se.name = sed.parent
        LEFT JOIN 
            `tabSales Team` AS st ON se.name = st.parent
        WHERE 
            {conditions} 
            AND se.docstatus = 1 
            AND se.stock_entry_type = (
                SELECT name 
                FROM `tabStock Entry Type` 
                WHERE matrial_type = 'Dispensing Simples'
            )
    """
    result = frappe.db.sql(sql_query, as_dict=True)
    
    # for row in result:
    #     if row['recovered'] == 0:
    #         row['residual'] = row['outgoing']
    
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


