// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Purchases by Cost Center"] = {
	"filters": [
		{
			"fieldname":"period_start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 0,
		},
		{
			"fieldname":"period_end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 0,
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"reqd" :0
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
            fieldname: "supplier_name",
            label: __("Supplier Name"),
            fieldtype: "Data",
        },
        {
            fieldname: "supplier_group",
            label: __("Supplier Group"),
            fieldtype: "Link",
            options: "Supplier Group",
        },
		{
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: [
                { "label": "Draft", "value": "Draft" },
                { "label": "Return", "value": "Return" },
                { "label": "Debit Note Issued", "value": "Debit Note Issued" },
				{ "label": "Submitted", "value": "Submitted" },
                { "label": "Paid", "value": "Paid" },
                { "label": "Partly Paid", "value": "Partly Paid" },
				{ "label": "Unpaid", "value": "Unpaid" },
                { "label": "Overdue", "value": "Overdue" },
                { "label": "Internal Transfer", "value": "Internal Transfer" },
            ]
        },
        {
            fieldname: "territory",
            label: __("Territory"),
            fieldtype: "Link",
            options: "Territory",
        },
		{
            "fieldname":"is_return",
            "label": __("Is Return"),
            "fieldtype": "Check",
        },
		// {
        //     "fieldname": "operation",
        //     "label": __("Operation"),
        //     "fieldtype": "Select",
        //     "options": "\n>\n<"
        // },
		// {
        //     "fieldname": "value",
        //     "label": __("Value"),
        //     "fieldtype": "Data",
        //     // "options": "\n>\n<"
        // }
	]
};
