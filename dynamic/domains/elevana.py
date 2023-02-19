from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Lead': [
            {
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "campaign_name",
                "label": "Sales Person",
                "options": "Sales Person",
                "permlevel":"1"
            }
        ],

        'Opportunity': [
            {
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "source",
                "label": "Sales Person",
                "options": "Sales Person",
                # "permlevel":"1"
            }
        ],
        'Customer': [
            {
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "opportunity_name",
                "label": "Sales Person",
                "options": "Sales Person",
                # "permlevel":"1"
            }
        ],
        'Quotation': [
            {
                "fieldname": "sales_team_section_break",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule",
                "label": "Sales Team",
            },
            {
                "fieldname": "sales_team",
                "fieldtype": "Table",
                "insert_after": "sales_team_section_break",
                "label": "Sales Team",
                "options" : "Sales Team"
            }
        ]

    },
    "properties": [

    ],
    "property_setters": [

    ],
    'on_setup': 'dynamic.elevana.setup.install_elevana'
}
