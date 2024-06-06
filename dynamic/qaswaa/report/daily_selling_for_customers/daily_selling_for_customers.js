// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily selling for customers"] = {
	"filters": [
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 0,
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 0,
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center" ,
			"reqd": 0,
		},
		{
			"fieldname":"set_warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options" : "Warehouse"
		},
		{
			"fieldname":"customer_name",
			"label": __("Customer Name"),
			"fieldtype": "Link",
			"options" : "Customer"
		},
		{
			"fieldname":"sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person"
		},
		{
			"fieldname":"sales_partner",
			"label": __("Sales Partner"),
			"fieldtype": "Link",
			"options": "Sales Partner"
		},
		{
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "MultiSelect",
            "options": "\nDraft\nReturn\nCredit Note Issued\nSubmitted\nPaid\nPartly Paid\nUnpaid\nUnpaid and Discounted\nPartly Paid and Discounted\nOverdue and Discounted\nOverdue\nCancelled\nInternal Transfer"
        }

	]
};
