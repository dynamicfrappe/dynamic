// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Deliveries Item depend om Customer"] = {
	"filters": [
		{
			"fieldname":"customer_id",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options":"Customer",
		},
		{
			"fieldname":"sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options":"Sales Person",
		},
	]
};
