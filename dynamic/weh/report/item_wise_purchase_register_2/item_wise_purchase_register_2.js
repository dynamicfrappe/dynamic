// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item-wise Purchase Register 2"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "MultiSelectList",
			options: "Item",
			"reqd": 0,
			get_data: function(txt) {
				return frappe.db.get_link_options('Item', txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			}
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
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"mode_of_payment",
			"label": __("Mode of Payment"),
			"fieldtype": "Link",
			"options": "Mode of Payment"
		},
		{
			"label": __("Group By"),
			"fieldname": "group_by",
			"fieldtype": "Select",
			"options": ["Supplier", "Item Group", "Item", "Invoice"]
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	}
}
