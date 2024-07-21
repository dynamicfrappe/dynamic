// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchases Analytics Cost Center"] = {
	"filters": [
	{
		fieldname: "period_start_date",
		label: __("From Date"),
		fieldtype: "Date",
		default: frappe.datetime.get_today(),
		reqd : 1
	},
	{
		fieldname: "period_end_date",
		label: __("To Date"),
		fieldtype: "Date",
		default: frappe.datetime.add_days(frappe.datetime.get_today(),10),
		reqd : 1
	},
    {
      fieldname: "item_code",
      label: __("Item"),
      fieldtype: "Link",
      options: "Item" ,
      reqd: 0
    },
    {
      fieldname: "item_group",
      label: __("Item Group"),
      fieldtype: "Link",
      options: "Item Group" ,
      reqd: 0
    },
    {
   fieldname: "supplier",
   label: __("Supplier"),
   fieldtype: "Link",
   options: "Supplier" ,
   reqd: 0
    },
    {
      fieldname: "cost_center",
      label: __("Cost Center"),
      fieldtype: "Link",
      options: "Cost Center" ,
      reqd: 0
    },
    
    {
         fieldname: "warehouse",
         label: __("Warehouse"),
         fieldtype: "Link",
         options: "Warehouse" ,
         reqd: 0
    }

   ]

};
