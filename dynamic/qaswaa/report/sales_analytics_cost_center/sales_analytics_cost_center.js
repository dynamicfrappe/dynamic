frappe.query_reports["Sales Analytics Cost Center"] = {
	"filters": [
      {
			fieldname: "period_start_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(),-10),
			reqd : 1
		},
		{
			fieldname: "period_end_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
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
   fieldname: "customer",
   label: __("Customer"),
   fieldtype: "Link",
   options: "Customer" ,
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
      },
      {
			"fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "reqd": 0
		},

   ]

}