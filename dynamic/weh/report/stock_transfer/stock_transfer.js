// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Transfer"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(),1),
			// reqd: 1
		},
		{
			label: __("From Warehouse"),
			fieldname: "from_warehouse",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Warehouse', txt, {
				});
			},
		},
		{
			label: __("To Warehouse"),
			fieldname: "to_warehouse",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Warehouse', txt, {
				});
			}
		},
		{
			"label": __("Item Code"),
			"fieldname":"item_code",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname":"parent_item_group",
			"label": __("Parent Item Group"),
			"fieldtype": "MultiSelectList",
			"options": "Item Group",
			get_data: function(txt){
				return frappe.db.get_link_options('Item Group', txt, {
					is_group: 1
				});
			}
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "MultiSelectList",
			"options": "Item Group",
			get_data: function(txt){
				
				let parent_item_group = frappe.query_report.get_filter_value('parent_item_group');
				if (parent_item_group.length == 0) {
					return frappe.db.get_link_options("Item Group", txt,{
						"is_group": 0
					});
				}else{
					return frappe.db.get_link_options("Item Group", txt,{
						"parent_item_group":["IN", parent_item_group]
					});
				};
			}
		},
	]
};
