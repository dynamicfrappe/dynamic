// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit Sales Invoice with last Purchase Invoice"] = {
	"filters": [
		{
			"fieldname":"sales_invoice",
			"label": __("Sales Invoice"),
			"fieldtype": "Link",
			"options":"Sales Invoice",
			"reqd": 1,
		},
	]
};
