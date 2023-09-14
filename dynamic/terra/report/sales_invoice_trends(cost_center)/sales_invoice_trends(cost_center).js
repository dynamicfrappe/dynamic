// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.require("assets/erpnext/js/sales_trends_filters.js", function() {
	frappe.query_reports["Sales Invoice Trends(Cost Center)"] = {
		filters: erpnext.get_sales_trends_filters()
	}
});