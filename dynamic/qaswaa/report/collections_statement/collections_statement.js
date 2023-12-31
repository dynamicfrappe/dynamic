// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Collections statement"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(),1),
		},
	]
};
