// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Analytics Customer Yearly"] = {
	"filters": [
		// {
		// 	"fieldname":"period_start_date",
		// 	"label": __("Start Date"),
		// 	"fieldtype": "Date",
		// 	"reqd": 1,
		// 	"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		// },
		// {
		// 	"fieldname":"period_end_date",
		// 	"label": __("End Date"),
		// 	"fieldtype": "Date",
		// 	"reqd": 1,
		// 	// "default": frappe.datetime.get_today()
		// },
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options" : "Fiscal Year",
		},
		{
			"fieldname":"fiscal_year1",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options" : "Fiscal Year",
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options" : "Cost Center",
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options" : "Warehouse",
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options" : "Customer",
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options" : "Item Group",
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options" : "Item",
		}
	]
};
