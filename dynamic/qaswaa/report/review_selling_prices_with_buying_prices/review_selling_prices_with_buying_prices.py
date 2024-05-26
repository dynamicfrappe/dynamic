# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data


def get_data(filters):
    selling_price_list = filters.get('selling')
    buying_price_list = filters.get('buying')
    conditions = "1=1"
    sql_params = [selling_price_list, buying_price_list]

    if filters.get("item_group"):
        conditions += f" AND i.item_group = '{filters.get('item_group')}'"  

    if selling_price_list and buying_price_list:
        sql = '''
            SELECT
                ip.item_code,
                ip.item_name,
                i.item_group,
                i.brand,
                MAX(CASE WHEN ip.selling = 1 THEN ip.price_list END) as price_list1,
                MAX(CASE WHEN ip.buying = 1 THEN ip.price_list END) as price_list2,
                MAX(CASE WHEN ip.selling = 1 THEN ip.price_list_rate END) as selling_price,
                MAX(CASE WHEN ip.buying = 1 THEN ip.price_list_rate END) as buying_price,
                (MAX(CASE WHEN ip.buying = 1 THEN ip.price_list_rate END) -
                MAX(CASE WHEN ip.selling = 1 THEN ip.price_list_rate END)) as price_difference,
                ROUND(((MAX(CASE WHEN ip.buying = 1 THEN ip.price_list_rate END) -
                MAX(CASE WHEN ip.selling = 1 THEN ip.price_list_rate END)) / MAX(CASE WHEN ip.selling = 1 THEN ip.price_list_rate END)) * 100, 2) as difference_percentage
            FROM
                `tabItem Price` ip
            INNER JOIN
                `tabItem` i ON ip.item_code = i.item_code
            WHERE
                ip.price_list IN (%s, %s)
                AND {conditions}
            GROUP BY
                ip.item_code, ip.item_name, i.item_group, i.brand
            '''
        sql = sql.format(conditions=conditions)
        items = frappe.db.sql(sql, tuple(sql_params), as_dict=True)

        return items
    else:
        return []




def get_columns(filters):
    columns = [
        {
			"fieldname": "item_code",
			"label": _("Item"),
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
			"fieldname": "price_list1",
			"label": _("Selling Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 200,
		},
        {
			"fieldname": "price_list2",
			"label": _("Buying Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"width": 200,
		},
        {
			"fieldname": "item_group",
			"label": _("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 200,
		},
        {
			"fieldname": "brand",
			"label": _("Brand"),
			"fieldtype": "Link",
			"options": "Brand",
			"width": 200,
		},
        {
            "fieldname": "selling_price",
            "label": _("Selling Price"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "fieldname": "buying_price",
            "label": _("Buying Price"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "fieldname": "price_difference",
            "label": _("Price Difference"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150,
        },
        {
            "fieldname": "difference_percentage",
            "label": _("Difference Percentage"),
            "fieldtype": "Data",
            "width": 150,
        },
	]
    return columns	
	






    


