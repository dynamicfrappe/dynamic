// Copyright (c) 2025, Dynamic and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["CRM sales report"] = {
    "filters": [
		{
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": [
				"all",
                "Lead", 
                "Open", 
                "Replied", 
                "Opportunity", 
                "Quotation", 
                "Lost Quotation", 
                "Interested", 
                "Converted", 
                "Do Not Contact"
				
            ],
            // "default": "all"
			
        },
        {
            "fieldname": "start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30) 
        },
        {
            "fieldname": "end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.get_today()
        },
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link", 
			"options":"Sales Person"
			// "description": __("Filter by Sales Person")
		},
		{   
			"fieldname": "Mobile_No",
			"label": __("PHONE"),
			"fieldtype": "Data", 
			
        }
        
    ]
}


