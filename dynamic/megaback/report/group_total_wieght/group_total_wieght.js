// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Group Total Wieght"] = {
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
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date"
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date"
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options:"Item Group"
		},
		{	
			"label": ("Item Parent  Group"),
			"fieldname": "parent_group",
			"fieldtype": "Link",
			"options" :"Item Group" ,
			"width": 200,
			"reqd" : 1 ,
			get_query: () => {
		
				return {
					filters: {
						'is_group': 1 ,
						
					}
				}
			}
		},
		
	]
};
