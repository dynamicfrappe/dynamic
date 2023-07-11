// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GL Edit Test"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1
		
		},
		// {
		// 	"fieldname":"show_items",
		// 	"label": __("Show Items"),
		// 	"fieldtype": "Check",
		// 	"defaulte": 1 ,
			
		
		// },
	],
	"tree": true,
	"name_field": "parent",
	"parent_field": "parent_invoice",
	"initial_depth": 3,
	"formatter": function(value, row, column, data, default_formatter) {
		// if (column.fieldname == "sales_invoice" && column.options == "Item" && data && data.indent == 0) {
		// 	column._options = "Sales Invoice";
		// } else {
		// 	column._options = "Item";
		// }
		value = default_formatter(value, row, column, data);

		if (data && (data.indent == 0 )) {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	}
};
