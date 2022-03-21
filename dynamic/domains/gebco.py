from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Item': [
            {
                "fieldname": "serial1",
                "fieldtype": "Data",
                "insert_after": "is_item_from_hub",
                "label": "Serial 1",
                "unique": 1,
                "reqd": 1,
            },
            {
                "fieldname": "serial2",
                "fieldtype": "Data",
                "insert_after": "serial1",
                "label": "Serial 2",
                "unique": 1,
            }
        ]
    },
    "properties": [

    ],
    "property_setters": [

    ],
    
}
