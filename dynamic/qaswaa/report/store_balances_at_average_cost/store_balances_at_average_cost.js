// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Store Balances at Average Cost"] = {


	"filters": [

					{

						"label": ("Company"),
						"fieldname": "company",
						"fieldtype": "Link",
						"options" :"Company" ,
						"width": 200,
						"reqd": 1,
						"default": frappe.defaults.get_user_default("Company")
					

					},
					{	"label": ("Date"),
						"fieldname": "date",
						"fieldtype": "Date",
						"width": 200,
					},
					{	
						"label": ("Warehouse"),
						"fieldname": "warehouse",
						"fieldtype": "Link",
						"options" :"Warehouse" ,
						"width": 200,
						get_query: () => {
							var company = frappe.query_report.get_filter_value('company');
							var parent  = frappe.query_report.get_filter_value('warehouse_group') 
							
							
							var filters  = {
											'is_group': 0 ,
											"company" : company 
											}
								if (parent){
									filters["parent_warehouse"] = parent
								}
								return {

								filters: filters
							}
						}
					},
					{
						"label": ("Item Group"),
						"fieldname": "item_group",
						"fieldtype": "Link",
						"options" :"Item Group" ,
						"width": 200,
					},
					{
						"label":("Tax Group"),
						"fieldname": "tax_group",
						"fieldtype": "Data",
						"width": 200,
					},
					{	
						"label":("Origin"),
						"fieldname": "origin",
						"fieldtype": "Link",
						"options" : "Origin" ,
						"width": 200,
					},
					{	
						"label": ("Brand"),
						"fieldname": "brand",
						"fieldtype": "Link",
						"options" : "Brand" ,
						"width": 200,
					},
					{	
						"label": ("Warehouse Group"),
						"fieldname": "warehouse_group",
						"fieldtype": "Link",
						"options" :"Warehouse" ,
						
						"width": 200,
						get_query: () => {
							var company = frappe.query_report.get_filter_value('company');
							return {
								filters: {
									'is_group': 1 ,
									"company" :company
								}
							}
						}
					},
					{
						"label": "Material",
						"fieldname": "material",
						"fieldtype": "Link",
						"options":"Material",
						"width": 200,
					},
					
				]
															}
	