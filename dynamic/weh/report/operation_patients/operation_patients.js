// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Operation patients"] = {
	"filters": [
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
