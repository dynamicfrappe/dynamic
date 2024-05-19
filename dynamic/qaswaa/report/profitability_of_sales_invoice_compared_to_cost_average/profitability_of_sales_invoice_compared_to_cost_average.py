# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from dynamic.qaswaa.utils.qaswaa_api import get_last_purchase_invoice_for_item



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1"
    
    if filters.get("customer"):
        conditions += f" AND sd.customer = '{filters.get('customer')}'"
    if filters.get("sales_order"):
        conditions += f" AND sd.name = '{filters.get('sales_order')}'"
    if filters.get("set_warehouse"):
        conditions += f" AND sd.set_warehouse = '{filters.get('set_warehouse')}'"
    if filters.get("selling_price_list"):
        conditions += f" AND sd.selling_price_list = '{filters.get('selling_price_list')}'"    
    if filters.get("from_date"):
        conditions += f" AND sd.transaction_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND sd.transaction_date <= '{filters.get('to_date')}'"
  
    if filters.get("cost_center"):
        sql_join += f"""
            INNER JOIN `tabSales Invoice Item` sii_cc ON so_cc.name = sii_cc.parent
            AND sii_cc.cost_center = '{filters.get('cost_center')}'
        """
        
    if filters.get("sales_person"):
        sql_join += f"""
            INNER JOIN `tabSales Team` sii_sp ON si_sp.name = sii_sp.parent
            AND sii_sp.sales_person = '{filters.get('sales_person')}'
        """   

    sql = f'''
		SELECT 
			so.name AS sales_invoice,
			item.item_code,
			item.item_name,
			item.qty,
			item.rate,
			(
				SELECT pii.rate
				FROM `tabPurchase Invoice Item` pii
				INNER JOIN `tabPurchase Invoice` pi ON pi.name = pii.parent
				WHERE pii.item_code = item.item_code
				ORDER BY pi.creation DESC
				LIMIT 1
			) AS purchase_invoice_rate,
			item.qty * (
				SELECT pii.rate
				FROM `tabPurchase Invoice` pi
				INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
				WHERE pii.item_code = item.item_code
				ORDER BY pi.creation DESC
				LIMIT 1
			) AS total_purchase,
			item.rate - (
				SELECT pii.rate
				FROM `tabPurchase Invoice` pi
				INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
				WHERE pii.item_code = item.item_code
				ORDER BY pi.creation DESC
				LIMIT 1
			) AS variance,
			(item.rate - (
				SELECT pii.rate
				FROM `tabPurchase Invoice` pi
				INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
				WHERE pii.item_code = item.item_code
				ORDER BY pi.creation DESC
				LIMIT 1
			)) * item.qty AS total_variance,
			CONCAT(
				ROUND(
					(
						(item.rate - (
							SELECT pii.rate
							FROM `tabPurchase Invoice` pi
							INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
							WHERE pii.item_code = item.item_code
							ORDER BY pi.creation DESC
							LIMIT 1
						)) / (
							SELECT pii.rate
							FROM `tabPurchase Invoice` pi
							INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
							WHERE pii.item_code = item.item_code
							ORDER BY pi.creation DESC
							LIMIT 1
						) * 100
					),
					2
				),
				'%'
			) AS variance_percentage
		FROM 
			`tabSales Invoice` so
		INNER JOIN
			`tabSales Invoice Item` item ON item.parent = so.name
        WHERE {conditions}
        '''

    data = frappe.db.sql(sql, as_dict=1)
    return data



def get_columns():
    columns = [
        {
            "fieldname": "sales_invoice",
            "label": _("Sales Invoice"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 300,
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "qty",
            "label": _("Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "rate",
            "label": _("Selling price"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "purchase_invoice_rate",
            "label": _("Purchase Invoice Rate"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_purchase",
            "label": _("Total Purchase"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "variance",
            "label": _("Variance"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_variance",
            "label": _("Total Variance"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "variance_percentage",
            "label": _("Variance Percentage"),
            "fieldtype": "Data",
            "width": 100,
            "options": "%"
        },
    ]
    return columns


