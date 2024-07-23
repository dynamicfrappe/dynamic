// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Analytics by Project"] = {
	"filters": [
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd" :1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
			"reqd": 1
		},
	]
};
