# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_data(filters): 
	conditions = " 1=1"
	# conditions = f" PII.item_code  = '{filters.get('item_code')}'" 
	
	if filters.get("from_date"): 
		conditions += " and PI.posting_date >= '%s'"%filters.get("from_date") 
	if filters.get("to_date"): 
		conditions += " and PI.posting_date <= '%s'"%filters.get("to_date") 
	
	sql = f''' 
		SELECT  
			PII.rate,  
			PI.posting_date,  
			PII.item_code,  
			PII.item_name, 
			ROW_NUMBER() OVER (PARTITION BY PII.item_code ORDER BY PI.posting_date) AS row_num 
		FROM  
			`tabPurchase Invoice` PI 
		JOIN  
			`tabPurchase Invoice Item` PII 
		ON  
			PII.parent = PI.name 
		WHERE 
			PI.docstatus = 1 and {conditions} 
	''' 
	
	data = frappe.db.sql(sql, as_dict=True) 
	result_dict = {}
	for entry in data:
		item_code = entry['item_code']
		row_num = entry['row_num']

		item_sql = f''' 
				SELECT 
					brand , material , origin , electroic_code ,
					old_code , description 
				FROM 
					`tabItem`
				WHERE 
					name = '{item_code}'
				'''
		item_data = frappe.db.sql(item_sql , as_dict = 1)

		if item_code not in result_dict:
			result_dict[item_code] = {'item_code': item_code, 'item_name': entry['item_name'] , 
							 'brand' : item_data[0]["brand"] , 'material' : item_data[0]["material"],
							 'origin' : item_data[0]["origin"] , 'electroic_code' : item_data[0]["electroic_code"],
							 'old_code' : item_data[0]["old_code"] , 'description' : item_data[0]["description"],

							 }

		result_dict[item_code][f'rate{row_num}'] = entry['rate']
		result_dict[item_code][f'posting_date{row_num}'] = entry['posting_date']

		# Set a limit for rates and posting dates (up to rate6 and posting_date6)
		# if row_num == 6:
		# 	break

	# Convert the result_dict to a list
	final_result = list(result_dict.values())
	# frappe.throw(str(final_result))

	return final_result

def get_columns(num_rates=6): 
    columns = [ 
        { 
            "label": _("Item Code"), 
            "fieldname": "item_code", 
            "fieldtype": "Link", 
            "options": "Item", 
            "width": 200, 
        }, 
        { 
            "label": _("Item Name"), 
            "fieldname": "item_name", 
            "fieldtype": "Data", 
            "width": 100, 
        }, 	
		{ 
            "label": _("Description"), 
            "fieldname": "description", 
            "fieldtype": "Text Editor", 
            "width": 200, 
        },
		{ 
            "label": _("Brand"), 
            "fieldname": "brand", 
            "fieldtype": "Link", 
            "options": "Brand", 
            "width": 60, 
        },		
		{ 
            "label": _("Material"), 
            "fieldname": "material", 
            "fieldtype": "Link", 
            "options": "Material", 
            "width": 80, 
        },		
		{ 
            "label": _("Origin"), 
            "fieldname": "origin", 
            "fieldtype": "Link", 
            "options": "Origin", 
            "width": 90, 
        },		
		{ 
            "label": _("Electroic Code"), 
            "fieldname": "electroic_code", 
            "fieldtype": "Link", 
            "options": "Electroic Code", 
            "width": 80, 
        },
		{ 
            "label": _("Old Code"), 
            "fieldname": "old_code", 
            "fieldtype": "Link", 
            "options": "Old Code", 
            "width": 80, 
        },		
    ] 
 
    for i in range(1, num_rates + 1): 
        columns.extend([ 
            { 
                "label": _("Rate {}".format(i)), 
                "fieldname": "rate{}".format(i), 
                "fieldtype": "Data", 
                "width": 100, 
            }, 
            { 
                "label": _("Posting Date {}".format(i)), 
                "fieldname": "posting_date{}".format(i), 
                "fieldtype": "Data", 
                "width": 120, 
            }, 
        ]) 
 
    return columns