from __future__ import unicode_literals

data = {
    
    'custom_fields': {
        "Customer":
        [ 
            {
                "label": "Discount Item",
                "fieldname": "discount_item",
                "fieldtype": "Float",
                "insert_after": "territory" ,
            },
        ],
        "Sales Order":
        [ 
            {
                "label": "Discount Item",
                "fieldname": "discount_item",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
                "fetch_from":"customer.discount_item",
            },
        ],
        "Sales Invoice":
        [ 
            {
                "label": "Discount Item",
                "fieldname": "discount_item",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
                "fetch_from":"customer.discount_item",
            },
        ],
           "Quotation":
        [ 
            {
                "label": "Discount Item",
                "fieldname": "discount_item",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
                "fetch_from":"party_name.discount_item",
            },
        ],

    },
    "properties": [

    ],
    "property_setters": [
    ],
    
}
