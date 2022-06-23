// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Actions Report"] = {
	// asd
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date"
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date"
		},
		{
			fieldname: "type",
			label: __("Type"),
			fieldtype: "Select",
			options:"\nIndoor\nOut door"
		},
		{
			fieldname: "actions",
			label: __("Action"),
			fieldtype: "Link",
			options:"Action"
		},
		{
			fieldname: "customer_type",
			label: __("Customer Type"),
			fieldtype: "Select",
			options:"\nLead\nOpportunity"
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options:"Branch"
		}
	]
};
