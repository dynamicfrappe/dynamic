// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Item sales"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			// default: frappe.datetime.get_today(),
			reqd : 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			// default: frappe.datetime.add_days(frappe.datetime.get_today(),1),
			reqd : 1
		},
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item" ,
			reqd: 1
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer" ,
			reqd: 1
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group" ,
			reqd: 1
		},
	]
};
