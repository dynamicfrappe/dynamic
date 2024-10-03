// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Amount of Each Curreny"] = {
	"filters": [
		{
			"fieldname": "currency",
			"label": __("Currency"),
			"fieldtype": "Link",
			"options": "Currency" ,
		},
		// {
		// 	"fieldname":"sales_invoice",
		// 	"label": __("Sales Invoice"),
		// 	"fieldtype": "Link",
		// 	"options":"Sales Invoice",
		// },
		{
			"fieldname": "account_type",
			"label": __("Account Type"),
			"fieldtype": "Select",
			"options": "\nbank\ncash" ,
		},

	]
};
