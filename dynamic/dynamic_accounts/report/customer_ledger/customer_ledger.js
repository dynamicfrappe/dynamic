// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Customer Ledger"] = {
	"filters": [
			{
				"fieldname":"company",
				"label": __("Company"),
				"fieldtype": "Link",
				"options": "Company",
				"default": frappe.defaults.get_user_default("Company"),
				"reqd": 1
			},
			{
				"fieldname":"from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
				"reqd": 1,
				"width": "60px"
			},
			{
				"fieldname":"to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"default": frappe.datetime.get_today(),
				"reqd": 1,
				"width": "60px"
			},
			{
				"fieldname": "customer",
				"label": __("Customer"),
				"fieldtype": "Link",
				"options": "Customer",
				"reqd": 1,
				on_change: () => {
					var customer = frappe.query_report.get_filter_value('customer');
					if (customer) {
						frappe.db.get_value('Customer', customer, "customer_name", function(value) {
							frappe.query_report.set_filter_value('customer_name', value["customer_name"]);
						});
					} else {
						frappe.query_report.set_filter_value('customer_name', "");
					}
				}
			},
			{
				"fieldname":"show_items",
				"label": __("Show Items"),
				"fieldtype": "Check",
				"defaulte": 1 ,
				
			
			},
			{
				"fieldname":"customer_name",
				"label": __("Customer Name"),
				"fieldtype": "Data",
				"hidden": 1
			}
	]
};
