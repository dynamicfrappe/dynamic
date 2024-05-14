// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compare quotation rates with item price"] = {
	"filters": [
		{
			"fieldname":"quotation",
			"label": __("Quotation"),
			"fieldtype": "Link",
			"options":"Quotation",
			"reqd": 1,
		},
		{
			"fieldname":"price_list",
			"label": __("Price List"),
			"fieldtype": "Link",
			"options":"Price List",
			"reqd": 1,
		},
		
	]
};
