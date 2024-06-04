# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 



def get_all_child_groups(group , childes= []) :

	def get_childs(): 
		if frappe.db.get_value("Item Group" , group , "is_group") :
		
			groups = frappe.get_all("Item Group" , {"parent_item_group" : group} , "name")
			for gr in groups :
				if  frappe.db.get_value("Item Group" , gr.get("name") , "is_group") :
					data =frappe.db.sql(f""" select name from 
							`tabItem Group` WHERE parent_item_group  = '{gr.get("name")}'""" ,as_dict=1)
					for name  in data :
						childes.append(name.get("name"))
						get_all_child_groups(name.get("name") , childes=childes)
				else :
					pass
		return childes				

		
	print(childes)
	return get_childs()
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
					WHERE SO.docstatus=1 
				"""
	if filters.get("from_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date >= date('{filters.get("from_date")}')"""
	if filters.get("to_date")  : 
		condetion = condetion + f""" AND  SO.transaction_date <= date('{filters.get("to_date")}')"""
	
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
	if filters.get("parent_group") :
		parents = get_all_child_groups(filters.get("parent_group"))
		parent_str="("
		for pr in parents :
			print(pr)
			parent_str += f"('{pr}') ,"
		parent_str+= f"""('{filters.get("parent_group")}' ) )"""
		print(parent_str)
		sql = f"""
				SELECT 
				IG.parent_item_group as item_group  ,
				SUM(SOI.total_weight) as total_weight  ,
				SOI.weight_uom as uom
				FROM `tabSales Order Item` SOI  
				INNER JOIN `tabSales Order` SO 
				ON SOI.parent = SO.name
				INNER JOIN `tabItem Group` IG
				ON SOI.item_group = IG.name
				WHERE IG.parent_item_group in {parent_str}
				GROUP BY IG.parent_item_group
	
			"""
		condetion = condetion + f""" AND SOI.item_group  in 
				(select name from 
				`tabItem Group` WHERE parent_item_group  = '{filters.get("parent_group")}')"""
	
	data = frappe.db.sql(sql ,as_dict =1)
	return data