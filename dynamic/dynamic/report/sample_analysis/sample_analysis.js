// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sample analysis"] = {
	"filters": [
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			// "reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default" : frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},
	]
};
