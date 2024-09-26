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
            {
                "label": "Total Price",
                "fieldname": "total_price",
                "fieldtype": "Currency",
                "insert_after": "total_billing_amount" ,
                "options": "currency",
                "read_only": 1

            },
            {
                "label": "Discount",
                "fieldname": "discount",
                "fieldtype": "Float",
                "insert_after": "total_price" ,
                "read_only": 1

            },                          
            {
                "label": "All Total",
                "fieldname": "all_total",
                "fieldtype": "Currency",
                "insert_after": "total_discount_amount" ,
                "options": "currency",
                "read_only": 1
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
