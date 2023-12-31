// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rehab Compound Info"] = {
	"filters": [
		// {
		// 	fieldname: "from_date",
		// 	label: __("From Date"),
		// 	fieldtype: "Date",
		//   },
		//   {
		// 	fieldname: "to_date",
		// 	label: __("To Date"),
		// 	fieldtype: "Date",
		//   },
		  {
			  label: __("Contract"),
			fieldname: "contract",
			fieldtype: "Link",
			options: "Rehab Contract",
		  },
		  {
			  label: __("Customer"),
			  fieldname: "customer",
			fieldtype: "Link",
			options: "Customer",
		  },
	]
};
