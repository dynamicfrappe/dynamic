// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Operation patients"] = {
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
			label: __("Doctor"),
			fieldname: "doctor",
			fieldtype: "Data",
		},
		{
			"label": __("Customer"),
			"fieldname":"customer",
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			label: __("surgery"),
			fieldname: "surgery",
			fieldtype: "Data",
		},
		{
			"label": __("Branch"),
			"fieldname":"branch",
			"fieldtype": "Data",
		},
	]
};
