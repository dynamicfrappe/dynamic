// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance in Warehouse From Sales Order"] = {
	"filters": [
		{
			"fieldname": "sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order"
		},
		{
			fieldname: "date",
			label: __("Date"),
			fieldtype: "Date",
			// default: frappe.datetime.get_today(),
			// reqd : 1
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			fieldname: "customer_name",
			label: __("Customer Name"),
			fieldtype: "Data",
			// reqd: 1
		},
		{
			"fieldname": "delivery_status",
			"label": __("Delivery Status"),
			"fieldtype": "Select",
			"options": 
			["Not Delivered",
			"Fully Delivered",
			"Partly Delivered",
			"Closed" ,
			"Not Applicable"
			]
		},
		{
			"fieldname": "billing_status",
			"label": __("Billing Status"),
			"fieldtype": "Select",
			"options": 
					["Not Billed",
					"Fully Billed",
					"Partly Billed",
					"Closed"
					]
		},

	]
};
