// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Compare quotation rates with item price"] = {
    "filters": [
        {
            "fieldname": "quotation",
            "label": __("Quotation"),
            "fieldtype": "Link",
            "options": "Quotation",
            "reqd": 0,
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
        },
        {
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center",
        },
        {
            "fieldname": "selling_price_list",
            "label": __("Selling Price List"),
            "fieldtype": "Link",
            "options": "Price List",
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
        },
    ]
};

