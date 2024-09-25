// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Buying from Suppliers"] = {
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
			"fieldname":"supplier_name",
			"label": __("Supplier Name"),
			"fieldtype": "Link",
			"options" : "Supplier"
		},
		{
			"fieldname":"supplier_group",
			"label": __("Supplier Group"),
			"fieldtype": "Link",
			"options" : "Supplier Group"
		},
		{
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "MultiSelect",
            "options": "\nDraft\nReturn\nDebit Note Issued\nSubmitted\nPaid\nPartly Paid\nUnpaid\nOverdue\nCancelled\nInternal Transfer"
        },
		{
            "fieldname": "operation",
            "label": __("Operation"),
            "fieldtype": "Select",
            "options": "\n>\n<"
        },
		{
            "fieldname": "value",
            "label": __("Value"),
            "fieldtype": "Data",
            // "options": "\n>\n<"
        },


	]
};
