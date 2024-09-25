// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchases Vouchers Items"] = {
	"filters": [
        {
            "fieldname": "item_code",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0
        },
		{
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options": "Item Group",
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
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "reqd": 0
        },
		{
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center",
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
	]
};
