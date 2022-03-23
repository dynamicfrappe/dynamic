from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Serial No': [
            {
                "fieldname": "serial2",
                "fieldtype": "Data",
                "insert_after": "serial_no",
                "label": "Serial No 2",
                "unique": 1,
            },
        ],
        'Sales Invoice': [
            {
                "fieldname": "maintenance_template",
                "fieldtype": "Link",
                "options":"Maintenance Template",
                "insert_after": "delivery_note",
                "label": "Maintenance Template",
                "print_hide": 1,
            },
        ],
        'Delivery Note': [
            {
                "fieldname": "maintenance_template",
                "fieldtype": "Link",
                "options":"Maintenance Template",
                "insert_after": "sales_team",
                "label": "Maintenance Template",
                "print_hide": 1,
            },
        ],
        'Stock Entry': [
            {
                "fieldname": "maintenance_template",
                "fieldtype": "Link",
                "options":"Maintenance Template",
                "insert_after": "is_return",
                "label": "Maintenance Template",
                "print_hide": 1,
            },
        ]
    },
    "properties": [

    ],
    "property_setters": [

    ],
    
}
