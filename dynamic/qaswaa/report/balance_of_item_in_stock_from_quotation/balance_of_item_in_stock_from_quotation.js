// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance of Item in Stock From Quotation"] = {
	"filters": [
		{
			fieldname: "date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			// reqd : 1
		},
		{
			"fieldname": "quotation_to",
			"label": __("Quotation To"),
			"fieldtype": "Link",
			"options": "DocType"
		},
		{
			"fieldname": "party_name",
			"label": __("Party"),
			"fieldtype": "DynamicLink",
			"options": "quotation_to"
		},
		{
			fieldname: "customer_name",
			label: __("Customer Name"),
			fieldtype: "Link",
			options: "Customer" ,
			// reqd: 1
		},
		{
			"fieldname": "quotation",
			"label": __("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation"
		},
		{
			"fieldname": "price_list",
			"label": __("Price List"),
			"fieldtype": "Link",
			"options": "Price List"
		},
	]
};
