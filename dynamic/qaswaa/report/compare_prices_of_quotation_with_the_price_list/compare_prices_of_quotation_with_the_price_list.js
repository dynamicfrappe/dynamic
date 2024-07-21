// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compare Prices of Quotation With The Price List"] = {
	"filters": [
		{
			fieldname: "date",
			label: __("Date"),
			fieldtype: "Date",
			// default: frappe.datetime.get_today(),
			// reqd : 1
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			fieldname: "party_name",
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
			"fieldname": "quotation",
			"label": __("Quotation"),
			"fieldtype": "Link",
			"options": "Quotation"
		},
		{
			"fieldname": "price_list",
			"label": __("Price List"),
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
	]
};
