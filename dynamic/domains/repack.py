
from __future__ import unicode_literals

data = {
    'custom_fields': {
        "Manufacturing Settings":[
            {
                "label": "Allow Show Bom Check",
                "fieldname": "allow_show_bom_check",
                "fieldtype": "Check",
                "insert_after": "material_consumption",
            },
            {
                "label": "Change Precent",
                "fieldname": "change_precent",
                "fieldtype": "Data",
                "insert_after": "allow_show_bom_check",
            }
        ],
        "Stock Entry":[
            {
                "label": "Repack",
                "fieldname": "repack",
                "fieldtype": "Link",
                "options": "Reback",
                "insert_after": "stock_entry_type",
                "read_only": "1",
            },
        ]
        #Stock Entry Type
       
},
"properties": [  
        #Sales Order Item
        {
        "doctype": "Stock Entry",
        "doctype_or_field": "DocField",
        "fieldname": "from_warehouse",
        "property": "read_only",
        "property_type": "Check",
        "value": "1",
        },
        {
        "doctype": "Stock Entry",
        "doctype_or_field": "DocField",
        "fieldname": "to_warehouse",
        "property": "read_only",
        "property_type": "Check",
        "value": "1",
        },
        {
        "doctype": "Stock Entry Detail",
        "doctype_or_field": "DocField",
        "fieldname": "qty",
        "property": "read_only",
        "property_type": "Check",
        "value": "1",
        },
]
}