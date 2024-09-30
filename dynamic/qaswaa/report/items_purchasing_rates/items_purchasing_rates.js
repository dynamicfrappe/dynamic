// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Items Purchasing Rates"] = {
	"filters": [
        {
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0
        },
        {
            "fieldname": "item_name",
            "label": __("Item_name"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "reqd": 0
        },
        {
            "fieldname": "supplier_name",
            "label": __("supplier_name"),
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "date_from",
            "label": __("Date From"),
            "fieldtype": "Date",
            "reqd": 0,
            "default": frappe.datetime.now_date()
        },
        {
            "fieldname": "date_to",
            "label": __("Date To"),
            "fieldtype": "Date",
            "reqd": 0,
            "default": frappe.datetime.now_date() 
        }
    ],
};
