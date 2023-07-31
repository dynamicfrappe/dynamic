// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Appartement Reserved"] = {
	"filters": [
		// {
		// 	fieldname: "from_date",
		// 	label: __("From Date"),
		// 	fieldtype: "Date"
		// },
		// {
		// 	fieldname: "to_date",
		// 	label: __("To Date"),
		// 	fieldtype: "Date"
		// },
		{
			fieldname: "item_code",
			label: __("Item"),
			fieldtype: "Link",
			options:"Item"
		},
	],


	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "status" && data && data.status == 'Sold') {
			value = "<span style='color:red'>" + value + "</span>";
			// row = "<span style='color:red'>" + row + "</span>";
			// $(row).css("background-color", "red");
			// console.log($(row))
			// console.log(row)
		}
		// else if (column.fieldname == "in_qty" && data && data.in_qty > 0) {
		// 	value = "<span style='color:green'>" + value + "</span>";
		// }

		return value;
	}
};
