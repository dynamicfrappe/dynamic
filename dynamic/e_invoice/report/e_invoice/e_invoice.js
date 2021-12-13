// Copyright (c) 2016, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["E Invoice"] = {
	"filters": [
			{
			"fieldname":"start_date",
			"label": ("From  Date"),
			"fieldtype": "Date",

		},
		{
			"fieldname":"end_date",
			"label": ("To Date"),
			"fieldtype": "Date",

		},
		{
			"fieldname":"customer",
			"label": ("Customer"),
			"fieldtype": "Link",
			"options": "Customer"

		},
	]
};
