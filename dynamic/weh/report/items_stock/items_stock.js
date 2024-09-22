// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Items Stock"] = {
	"filters": [
			// {
			// 	"fieldname":"company",
			// 	"label": __("Company"),
			// 	"fieldtype": "Link",
			// 	"options": "Company",
			// 	"default": frappe.defaults.get_user_default("Company"),
			// 	"reqd": 1
			// },
			{
				fieldname: "warehouse",
				label: __("Warehouse"),
				fieldtype: "Link",
				options: "Warehouse",
				// get_data: function(txt) {
				// 	return frappe.db.get_link_options('Warehouse', txt, {
				// 		company: frappe.query_report.get_filter_value("company")
				// 	});
				// },
				// reqd: "1",
			},
			{
				"fieldname":"item_code",
				"label": __("Item Code"),
				"fieldtype": "Link",
				"options": "Item",
			},
			{
				"fieldname":"brand",
				"label": __("Category"),
				"fieldtype": "Link",
				"options": "Brand",
			},
			{
				"fieldname":"parent_group",
				"label": __("Parent Group"),
				"fieldtype": "Link",
				"options": "Item Group",
			},
			{
				"fieldname":"item_group",
				"label": __("Item Group"),
				"fieldtype": "Link",
				"options": "Item Group",
			},
			
	]
};
