
from __future__ import unicode_literals
import frappe
from frappe import _

data = {

	'custom_fields': {
		"Sales Order":
		[ 
			{
				"label": "Notes",
				"fieldname": "notes",
				"fieldtype": "Small Text",
				"insert_after": "to_date" ,
			},
		],
		"Quotation":
		[ 
		   
			{
				"label": "Sales Team",
				"fieldname": "sales_team_section_break_",
				"fieldtype": "Section Break",
				"insert_after": "payment_schedule" ,
			},
			{
				"label": "Sales Team Qt",
				"fieldname": "sales_team_qt",
				"fieldtype": "Table",
				"insert_after": "sales_team_section_break_" ,
				"options":"Sales Team",
			},
			{
				"label": "Notes",
				"fieldname": "notes",
				"fieldtype": "Small Text",
				"insert_after": "source" ,
			},
		
		],
		"Quotation Item":
		[ 
		   
			{
				"label": "Item Name Print",
				"fieldname": "item_name_print",
				"fieldtype": "Data",
				"insert_after": "item_name" ,
			},
		],
		"Item Group":
		[ 
		   
			{
				"label": "Group Code",
				"fieldname": "group_code",
				"fieldtype": "Data",
				"insert_after": "column_break_5" ,
			},
		
		],
		"Sales Invoice":
		[ 
			{
				"label": "Customer Name.",
				"fieldname": "customer_name_hand",
				"fieldtype": "Data",
				"insert_after": "customer_name" ,
			},
			{
				"label": "Notes",
				"fieldname": "notes",
				"fieldtype": "Small Text",
				"insert_after": "to_date" ,
			},
		],
		"Selling Settings":
		[
			{
				"label": "Apply Reservation",
				"fieldname": "apply_reservation",
				"fieldtype": "Check",
				"insert_after": "territory" ,
			},
		],
		"Stock Entry Type":
		[
			{
				"label": "Mendatory Fields",
				"fieldname": "mendatory_fields",
				"fieldtype": "Check",
				"insert_after": "purpose" ,
			},
		],
		"Stock Entry":
		[
			 {
				"label": "Mendatory Fields",
				"fieldname": "mendatory_fields",
				"fieldtype": "Check",
				"insert_after": "sales_team" ,
				"fetch_from":"stock_entry_type.mendatory_fields",
				# "hidden": 1
			},
			{
				"label": "Customer",
				"fieldname": "customer_id",
				"fieldtype": "Link",
				"insert_after": "stock_entry_type",
				"options": "Customer",
				"depends_on":"eval:doc.mendatory_fields == true",
				"mandatory_depends_on":"eval:doc.mendatory_fields == true"
			},
			{
				"label": "Sales Team",
				"fieldname": "sales_team",
				"fieldtype": "Table",
				"insert_after": "get_stock_and_rate",
				"options": "Sales Team",
				"depends_on": "eval:doc.mendatory_fields == true",
			},
		],
		"Item":
		[
			{
				"label": "Material",
				"fieldname": "material",
				"fieldtype": "Link",
				"insert_after": "brand" ,
				"options":"Material",
			},
			{
				"label": "Origin",
				"fieldname": "origin",
				"fieldtype": "Link",
				"insert_after": "material" ,
				"options":"Origin",
			},
			{
				"label": "Electroic Code",
				"fieldname": "electroic_code",
				"fieldtype": "Link",
				"insert_after": "origin" ,
				"options":"Electroic Code",
			},
 
			{
				"label": "Size",
				"fieldname": "size_",
				"fieldtype": "Link",
				"insert_after": "electroic_code" ,
				"options":"Size",
			},
			{
				"label": "Group Code",
				"fieldname": "group_code",
				"fieldtype": "Data",
				"insert_after": "size_" ,
			},
			{
				"label": "Objective",
				"fieldname": "objective_",
				"fieldtype": "Link",
				"insert_after": "group_code" ,
				"options":"Objective",
			},
		]
	},
	 "properties": [
		{
		# "doctype": "Sales Invoice",
		# "doctype_or_field": "DocField",
		# "fieldname": "customer_name",
		# "property": "read_only",
		# "property_type": "Check",
		# "value": "0"
		},
	 ]
}