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
                "label": "Set Discount",
                "fieldname": "set_discount",
                "fieldtype": "Button",
                "insert_after": "update_stock" ,
            },
            {
                "label": "Discount Item",
                "fieldname": "discount_item",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
                "fetch_from":"customer.discount_item",
            },
            {
                "fieldname": "cutomer_section_break",
                "fieldtype": "Section Break",
                "insert_after": "total_billing_hours",
                "label": "Customer Discount",
            },
            {
                "label": "Total Before Discount",
                "fieldname": "total_price",
                "fieldtype": "Currency",
                "insert_after": "cutomer_section_break" ,
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
                "label": "Total After Discount",
                "fieldname": "all_total",
                "fieldtype": "Currency",
                "insert_after": "total_discount_amount" ,
                "options": "currency",
                "read_only": 1
            },
        ],
            "Sales Invoice Item":
        [
            {
                "label": "Total Item Price",
                "fieldname": "total_item_price",
                "fieldtype": "Currency",
                "insert_after": "base_price_list_rate" ,
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
