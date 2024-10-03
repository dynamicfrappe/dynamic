// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compare Prices of Sales Order With Price List"] = {
	"filters": [
		{
			fieldname: "date",
			label: __("Date"),
			fieldtype: "Date",
			// default: frappe.datetime.get_today(),
			// reqd : 1
		},
		{
			"fieldname": "set_warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer" ,
			// reqd: 1
		},
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person"
		},
		{
			"fieldname": "sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order"
		},
		{
			"fieldname": "selling_price_list",
			"label": __("Selling Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"get_query": function() {
				return {
					"filters": {
						"selling": 1
					}
				};
			},
		},
		{
			"fieldname": "buying_price_list",
			"label": __("Buying Price List"),
			"fieldtype": "Link",
			"options": "Price List",
			"get_query": function() {
				return {
					"filters": {
						"buying": 1
					}
				};
			},
		},
	]
};

