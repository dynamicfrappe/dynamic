// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Transfer"] = {
	"filters": [
		{
			label: __("From Warehouse"),
			fieldname: "s_warehouse",
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			"label": __("Item Code"),
			"fieldname":"item_code",
			"fieldtype": "Link",
			"options": "Item",
		},
	]
};
