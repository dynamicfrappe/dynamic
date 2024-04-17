// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly sales for sales person"] = {
	"filters": [
		{
			"fieldname":"period_start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			"fieldname":"period_end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.get_today()
		},

		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options" : "Cost Center",
			// "reqd": 1,
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options" : "Warehouse",
			// "reqd": 1,
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options" : "Customer",
			// "reqd": 1,
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options" : "Item Group",
			// "reqd": 1,
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options" : "Item",
			// "reqd": 1,
		}
	]
};
