// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Document report"] = {
    "filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd" : 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd" : 0
		},
		{
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center",
            "reqd": 0 
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "reqd": 0 
        },
		{
            "fieldname": "driver",
            "label": __("Driver"),
            "fieldtype": "Link",
            "options": "Driver Name",
            "reqd": 0 
        },
		{
			"fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 0
		},
		{
			"fieldname": "sales_partner",
            "label": __("Sales Partner"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "reqd": 0
		},
		{
			"fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "reqd": 0
		}

    ]
};


