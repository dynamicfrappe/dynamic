// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Units Invoices Details"] = {
	"filters": [
        {
			label: "Customer",
			fieldname: "customer",
			fieldtype: "Link",
			options: "Customer",
		},
		{
			label: "Sales Invoice",
			fieldname: "sales_invoice",
			fieldtype: "Link",
			options: "Sales Invoice",
		},
		{
			label: "Subscription Plan",
			fieldname: "subscription_plan",
			fieldtype: "Link",
			options: "Subscription Plan",
		}
    ],

	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "customer" || 
			column.fieldname === "unit_area" || 
			column.fieldname === "invoice_name" || 
			column.fieldname === "status" || 
			column.fieldname === "total" ||
			column.fieldname === "fine_percent" || 
			column.fieldname === "num_of_delay_days" ||
			column.fieldname === "item_name" || 
			column.fieldname === "total_with_fine" ) {
			
			value = `<div style="text-align: center;">${value}</div>`;
		}


		return value;
	}
};
