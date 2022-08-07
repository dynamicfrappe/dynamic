// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Hardware Installation Summary"] = {
	"filters": [
		{
			fieldname: "from_time",
			label: __("From Time"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		  },
		  {
			fieldname: "to_time",
			label: __("To time"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		  },
		  {
			fieldname:"sales_order",
			label:__("Sales Order"),
			fieldtype:"Link",
			options:"Sales Order"
		  },
		  {
			fieldname:"installation_order",
			label:__("Installation Order"),
			fieldtype:"Link",
			options:"Installation Order"
		  },
		  {
			fieldname:"installation_request",
			label:__("Installation Request"),
			fieldtype:"Link",
			options:"Installation Request"
		  }
	]
};
