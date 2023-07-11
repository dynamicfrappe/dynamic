// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GL Edit Test"] = {
	"filters": [

	],
	"tree": true,
	"name_field": "parent",
	"parent_field": "parent_invoice",
	"initial_depth": 3,
	"formatter": function(value, row, column, data, default_formatter) {
		// if (column.fieldname == "sales_invoice" && column.options == "Item" && data && data.indent == 0) {
		// 	column._options = "Sales Invoice";
		// } else {
		// 	column._options = "Item";
		// }
		value = default_formatter(value, row, column, data);

		if (data && (data.indent == 0 )) {
			// console.log(data)
			console.log('value-->',value)
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	}
};
