// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Inventory Replenishment to Reorder Level"] = {
	"filters": [
		{
			fieldname : "item_code",
			label : __("ID"),
			fieldtype : "Link",
			options : "Item",
		},
		{
			fieldname : "item_name",
			label : __("Item Name"),
			fieldtype : "Data",
		},
		{
			fieldname : "warehouse",
			label : __("Warehouse"),
			fieldtype : "Link",
			options : "Warehouse",
		}
	]
};
