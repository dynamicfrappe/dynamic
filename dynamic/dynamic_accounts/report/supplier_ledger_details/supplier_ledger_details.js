// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier Ledger Details"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"reqd": 1
		
		},
		{
			"fieldname":"show_items",
			"label": __("Show Items"),
			"fieldtype": "Check",
			"defaulte": 1 ,
			
		
		},
	]
};
