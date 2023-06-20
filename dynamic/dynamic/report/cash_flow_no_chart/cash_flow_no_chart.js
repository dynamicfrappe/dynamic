// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Cash Flow No Chart"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('Cash Flow No Chart', 10);

	// The last item in the array is the definition for Presentation Currency
	// filter. It won't be used in Cash Flow No Chart for now so we pop it. Please take
	// of this if you are working here.

	frappe.query_reports["Cash Flow No Chart"]["filters"].splice(8, 1);

	frappe.query_reports["Cash Flow No Chart"]["filters"].push(
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});