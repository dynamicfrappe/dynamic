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
	"""
	Tables 
	SOI Sales Order Item 
	SO Sales Order 

	
	"""

	condetion = """ 
					WHERE 1=1 
				"""
	if filters.get("from_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date >= date('{filters.get("from_date")}')"""
	if filters.get("to_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date <= date('{filters.get("to_date")}')"""
	if filters.get("parent_group") :
		condetion = condetion + f""" AND SOI.item_group  in 
				(select name from 
				`tabItem Group` WHERE parent_item_group  = '{filters.get("parent_group")}')"""
	if filters.get("item_group") :
		condetion = condetion +f"""AND SOI.item_group = '{filters.get("item_group")}'"""


	
	sql = f"""
	SELECT 
	SOI.item_group as item_group  ,
	SUM(SOI.total_weight) as total_weight  ,
	SOI.weight_uom as uom
	FROM `tabSales Order Item` SOI  
	INNER JOIN `tabSales Order` SO
	{condetion}
	GROUP BY SOI.item_group
	
	"""
	data = frappe.db.sql(sql ,as_dict =1)
	return data