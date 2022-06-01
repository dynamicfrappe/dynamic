// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cheques Report_"] = {
	"filters": [
		{
			fieldname: 'payment_type',
			label: __('Payment Type'),
			fieldtype: 'Select',
			"options":["",'Pay','Receive']
			// depends_on: 'eval:doc.owner=="admin@admin.com"'
			// default: frappe.datetime.get_today(),
			// reqd: 1
		},
		{
			fieldname: 'cheque_status',
			label: __('Cheque Status'),
			fieldtype: 'Select',
			options:["",'New','Under Collect',"Rejected in Bank","Collected","Endorsed",'Paid']

		},
		{
			fieldname: 'from_date',
			label: __('From Date'),
			fieldtype: 'Date',
			// depends_on: 'eval:doc.owner=="admin@admin.com"'
			// default: frappe.datetime.get_today(),
			// reqd: 1
		},
		{
			fieldname: 'to_date',
			label: __('To Date'),
			fieldtype: 'Date',

		},
		{
			fieldname: "bank",
			label: __("Bank"),
			fieldtype: "Link",
			options: "Bank",
		},
		{
			fieldname: "bank_account",
			label: __("Bank Account"),
			fieldtype: "Link",
			options: "Bank Account",
		},
		
	]
};
