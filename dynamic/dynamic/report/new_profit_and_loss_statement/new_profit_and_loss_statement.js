// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["New Profit and Loss Statement"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('New Profit and Loss Statement', 10);

	frappe.query_reports["New Profit and Loss Statement"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		},{
			"fieldname": "account",
			"label": __("Cost of good sold account"),
			"fieldtype": "Link",
			"options":"Account"
		}
	);
});