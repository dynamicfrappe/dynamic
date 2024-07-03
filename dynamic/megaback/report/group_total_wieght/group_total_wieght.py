# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 



def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters =None) :
	columns= [
		{
            "label": _("Item Group "),
            "fieldname": "item_group",
            "fieldtype": "Data",
	        #"options" : "Item Group" , 
            "width": 250
        },
	    {
            "label": _("Total Weight"),
            "fieldname": "total_weight",
            "fieldtype": "Data",
            "width": 200
        },
		{
            "label": _("UOM"),
            "fieldname": "uom",
            "fieldtype": "Link",
	    	"options" : "UOM" ,
            "width": 200
        },
	]
	return columns



def get_data(filters=None) :
	data = []
	parent = filters.get("parent_group") 
	if not parent :
		return data 

	condetion = """ 
					WHERE SO.docstatus=1 
				"""
	if filters.get("from_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date >= date('{filters.get("from_date")}')"""
	if filters.get("to_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date <= date('{filters.get("to_date")}')"""
	parent_child_list = frappe.db.sql(f""" SELECT name ,lft ,rgt  FROM `tabItem Group` WHERE
							parent_item_group = '{parent}' """ ,as_dict=1)
	for parent_group in parent_child_list :



		
		
		sql = f"""
		SELECT 
		'{parent_group.get("name")}' as item_group ,
		'KG' as uom ,
		COALESCE(SUM(SOI.total_weight) ,0) as total_weight  
		FROM `tabSales Order Item` SOI  
		INNER JOIN `tabSales Order` SO  ON SO.name = SOI.parent
		INNER  JOIN `tabItem Group`  IG ON SOI.item_group = IG.name
		{condetion}
		AND
		 SOI.item_group in (SELECT name FROM `tabItem Group` WHERE rgt < {parent_group.get("rgt")}  
		AND  rgt > '{parent_group.get("lft")}'  ) 
					OR SOI.item_group ='{parent_group.get("name")}'
	
		
		"""

		data_l = frappe.db.sql(sql ,as_dict=1)
		data = data +data_l
		
	
	return data
