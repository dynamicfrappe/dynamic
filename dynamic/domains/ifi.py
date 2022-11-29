

from __future__ import unicode_literals
installation_status = [
    "",
    "Pending",
    "Start",
    "Inprogress",
    "Completed",
]

data = {

    'custom_fields': {
         'Quotation':[
            {
                "fieldname": "crean",
                "fieldtype": "Check",
                "insert_after": "customer_name",
                "label": "Crean",
            },
         ],
         'Opportunity':[
            {
                "label": "Opportunity Status",
                "fieldname": "oportunity_status",
                "fieldtype": "Link",
                "options":"Opportunity Status",
                "insert_after": "expected_closing",
            },
         ],
         'Sales Order':[
            {
                "label": "Sales Installation",
                "fieldname": "sales_installation",
                "fieldtype": "Select",
                "options":"\n".join(installation_status),
                "default":"",
                "insert_after": "more_info",
                "read_only" : 1,
                "allow_on_submit": 1    
            },
         ],
         'Lead':[
            {
                "label": "URL",
                "fieldname": "url",
                "fieldtype": "Data",
                "insert_after": "email_id",
                "allow_on_submit": 1    
            },
            {
                "label": "Check Url",
                "fieldname": "check_url",
                "fieldtype": "Button",
                "insert_after": "url",
            },
         ],
         'Customer':[
            {
                "label": "URL",
                "fieldname": "url",
                "fieldtype": "Data",
                "insert_after": "opportunity_name",
                "allow_on_submit": 1    
            },
            {
                "label": "Check Url",
                "fieldname": "check_url",
                "fieldtype": "Button",
                "insert_after": "url",
            },
         ],
         'Supplier':[
            {
                "label": "URL",
                "fieldname": "url",
                "fieldtype": "Data",
                "insert_after": "tax_withholding_category",
                "allow_on_submit": 1    
            },
            {
                "label": "Check Url",
                "fieldname": "check_url",
                "fieldtype": "Button",
                "insert_after": "url",
            },
         ],
    },
      "properties": [
        {
        "doctype": "Quotation",
        "doctype_or_field": "DocField",
        "fieldname": "payment_schedule",
        "property": "allow_on_submit",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Item",
        "doctype_or_field": "DocField",
        "fieldname": "delivered_by_supplier",
        "property": "default",
        "property_type": "Text",
        "value": "1",
        "default_value":1
        },
        {
        "doctype": "Sales Order Item",
        "doctype_or_field": "DocField",
        "fieldname": "delivery_date",
        "property": "in_list_view",
        "property_type": "Check",
        "value": 0,
        "default_value":0
        },
        
    ],
  
    'on_setup': 'dynamic.ifi.setup.setup_ifi'
}