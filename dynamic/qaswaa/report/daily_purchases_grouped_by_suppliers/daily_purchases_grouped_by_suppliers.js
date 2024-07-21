// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Purchases Grouped by Suppliers"] = {
	"filters": [
		{
			"fieldname":"period_start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname":"period_end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center"
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
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
			"options": "Company"
		},
	]
};
