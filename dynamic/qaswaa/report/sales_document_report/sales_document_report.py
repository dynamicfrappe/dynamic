# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data
# def get_data(filters):
# 	conditions = " 1=1"
# 	if filters.get("customer"):
# 		conditions += f" AND sd.customer = '{filters.get('customer')}'"
# 	if filters.get("driver"):
# 		conditions += f" AND sd.driver = '{filters.get('driver')}'"		
# 	# if filters.get("cost_center"):
# 	# 	sql_join += """
# 	# 		INNER JOIN `tabSales Invoice` si_cc ON sd.invoice_name = si_cc.name
# 	# 		INNER JOIN `tabSales Invoice Item` sii_cc ON si_cc.name = sii_cc.parent
# 	# 	"""
# 	# 	conditions += f" AND sii_cc.cost_center = '{filters.get('cost_center')}'"
# 	# if filters.get("warehouse"):
# 	# 	sql_join += """
# 	# 		INNER JOIN `tabSales Invoice` si_wh ON sd.invoice_name = si_wh.name
# 	# 		INNER JOIN `tabSales Invoice Item` sii_wh ON si_wh.name = sii_wh.parent
# 	# 	"""
# 	# 	conditions += f" AND sii_wh.warehouse = '{filters.get('warehouse')}'"
# 	# if filters.get("sales_person"):
# 	# 	sql_join += """
# 	# 		INNER JOIN `tabSales Invoice` si_sp ON sd.invoice_name = si_sp.name
# 	# 		INNER JOIN `tabSales Team` sii_sp ON si_sp.name = sii_sp.parent
# 	# 	"""
# 	# 	conditions += f" AND sii_sp.sales_person = '{filters.get('sales_person')}'"
# 	# if filters.get("sales_partner"):
# 	# 	sql_join += """
# 	# 		INNER JOIN `tabSales Invoice` si_partner ON sd.invoice_name = si_partner.name
# 	# 	"""
# 	# 	conditions += f" AND si_partner.sales_partner = '{filters.get('sales_partner')}'"

# 	if filters.get("from_date"):
# 		conditions += f" AND sd.posting_date >= '{filters.get('from_date')}'"
# 	if filters.get("to_date"):
# 		conditions += f" AND sd.posting_date <= '{filters.get('to_date')}'"

# 	sql = f'''
# 		SELECT 
# 			sd.posting_date , sd.invoice_name , sd.customer , sd.grand_total ,
# 			sd.collection , sd.delivery_type , sd.delivered_date ,
# 			sd.sales_person_notes , sd.shipping_company, sd.policy_number ,
# 			sd.driver , sd.delivered
# 		FROM 
# 			`tabSales Document States` sd
# 		WHERE 
# 			{conditions}
# 		'''
# 	data = frappe.db.sql(sql , as_dict = 1)

	
# 	return data
def get_data(filters):
    conditions = " 1=1"
    
    if filters.get("customer"):
        conditions += f" AND sd.customer = '{filters.get('customer')}'"
    if filters.get("sales_order"):
        conditions += f" AND sd.name = '{filters.get('sales_order')}'"
    if filters.get("set_warehouse"):
        conditions += f" AND sd.set_warehouse = '{filters.get('set_warehouse')}'"
    if filters.get("cost_center"):
        conditions += f" AND sd.cost_center = '{filters.get('cost_center')}'"
    if filters.get("selling_price_list"):
        conditions += f" AND sd.selling_price_list = '{filters.get('selling_price_list')}'"    
    if filters.get("from_date"):
        conditions += f" AND sd.transaction_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND sd.transaction_date <= '{filters.get('to_date')}'"
    if filters.get("sales_person"):
        conditions += f" AND sii_sp.sales_person = '{filters.get('sales_person')}'"

    sql = f'''
        SELECT 
            sd.name AS sales_order,
            item.item_code,
            item.item_name,
            item.qty,
            item.rate,
            (
                SELECT pii.rate
                FROM `tabPurchase Invoice` pi
                INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
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
            ) AS variance_percentage,
            (
                SELECT sii.rate
                FROM `tabSales Invoice` si
                INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
                WHERE sii.item_code = item.item_code
                ORDER BY si.creation DESC
                LIMIT 0,1
            ) AS last_price_1,
            (
                SELECT sii.rate
                FROM `tabSales Invoice` si
                INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
                WHERE sii.item_code = item.item_code
                ORDER BY si.creation DESC
                LIMIT 1,1
            ) AS last_price_2,
            (
                SELECT sii.rate
                FROM `tabSales Invoice` si
                INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
                WHERE sii.item_code = item.item_code
                ORDER BY si.creation DESC
                LIMIT 2,1
            ) AS last_price_3
        FROM 
            `tabSales Order` sd
        INNER JOIN
            `tabSales Order Item` item ON item.parent = sd.name
        LEFT JOIN
            `tabSales Team` sii_sp ON sii_sp.parent = sd.name 
        WHERE {conditions}
    '''
    data = frappe.db.sql(sql, as_dict=True)

    return data



def get_columns():
	columns = [
		{
			"fieldname": "posting_date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 300,
		},
		{
			"fieldname": "invoice_name",
			"label": _("Invoice Name"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 300,
		},
				{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 300,
		},
		{
			"fieldname": "grand_total",
			"label": _("Grand Total"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 300,
		},
		{
			"fieldname": "collection",
			"label": _("Collection"),
			"fieldtype": "Text",
			"width": 300,
		},
		{
			"fieldname": "delivery_type",
			"label": "Delivery Type",
			"fieldtype": "Link",
			"options": "Delivery Type",
			"width": 150,
		},
		{
			"fieldname": "delivered_date",
			"label": "Delivered Date",
			"fieldtype": "Date",
			"width": 150,
		},
		{
			"fieldname": "sales_person_notes",
			"label": "Sales Person Notes",
			"fieldtype": "Text",
			"width": 150,
		},
		{
			"fieldname": "shipping_company",
			"label": "Shipping Company",
			"fieldtype": "Link",
			"options": "Shipping Company",
			"width": 150,
		},
		{
			"fieldname": "policy_number",
			"label": "Policy number",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "driver",
			"label": "Driver",
			"fieldtype": "Link",
			"options":"Driver Name",
			"width": 150,
		},
		{
			"fieldname": "delivered",
			"label": "Delivered",
			"fieldtype": "Check",
			"width": 150,
		}
	]
	return columns
