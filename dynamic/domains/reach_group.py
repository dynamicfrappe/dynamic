
from __future__ import unicode_literals


data = {

    'custom_fields': {
        'Customer':[
            {
                "label": "Commercial Record",
                "fieldname": "commercial_record",
                "fieldtype": "Data",
                "insert_after": "tax_id",
            },
        ],
        'Payment Entry':[
            {
                "label": "Sales Person",
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "options": "Sales Person",
                "insert_after": "party_name",
            },
        ],
        'Journal Entry':[
            {
                "label": "Sales Person",
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "options": "Sales Person",
                "insert_after": "multi_currency",
            },
        ]
    },
    "properties": [
        {
        "doctype": "Customer",
        "doctype_or_field": "DocField",
        "fieldname": "customer_type",
        "property": "options",
        "property_type": "Text",
        "value": "Cash\nPayments\nPrePaid\nCompany\nIndividual",
        "default_value":"Cash"
        },
        
    ],

  

    'on_setup': 'dynamic.reach_group.setup.setup_reach'
}

