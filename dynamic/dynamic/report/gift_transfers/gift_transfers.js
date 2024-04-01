// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["gift transfers"] = {
	"filters": [
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			// "reqd": 1
		},
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			// "reqd": 1
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
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

