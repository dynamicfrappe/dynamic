frappe.query_reports["Review selling prices with buying prices"] = {
    "filters": [
        {
            "fieldname": "selling",
            "label": __("Selling Price List"),
            "fieldtype": "Link",
            "options": "Price List",
            "get_query": function() {
                return {
                    "filters": {
                        "selling": 1
                    }
                };
            },
            "reqd": 1 
        },
		{
            "fieldname": "buying",
            "label": __("Buying Price List"),
            "fieldtype": "Link",
            "options": "Price List",
            "get_query": function() {
                return {
                    "filters": {
                        "buying": 1
                    }
                };
            },
            "reqd": 1 
        }
    ]
};


