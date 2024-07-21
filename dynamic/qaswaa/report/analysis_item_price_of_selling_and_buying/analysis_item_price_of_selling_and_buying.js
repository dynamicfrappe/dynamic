// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Analysis Item Price of Selling and Buying"] = {
	"filters": [
		{
			"fieldname":"selling_price_list",
			"label": __("Selling Price List"),
			"fieldtype": "Link",
			"options":"Price List",
			"reqd": 1,
		},
		{
			"fieldname":"buying_price_list",
			"label": __("Buying Price List"),
			"fieldtype": "Link",
			"options":"Price List",
			"reqd": 1,
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		},
	]
};
