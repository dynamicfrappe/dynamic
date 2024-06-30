// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Transfer"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(),1),
			// reqd: 1
		},
		{
			label: __("From Warehouse"),
			fieldname: "s_warehouse",
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			"label": __("Item Code"),
			"fieldname":"item_code",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			fieldname: "parent_group",
			label: __("Parent Group"),
			fieldtype: "Link",
			options: "Item Group",
		  },
	]
};
