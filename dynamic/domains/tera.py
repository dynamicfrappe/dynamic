from __future__ import unicode_literals


data = {
    'custom_fields': {
        'Landed Cost Item': [
            {
                "fieldname": "rate_currency",
                "fieldtype": "Data",
                "insert_after": "rate",
                "label": "Price in supplier currency",
                'read_only' : 1
            },
               {
                "fieldname": "item_after_cost",
                "fieldtype": "Data",
                "insert_after": "rate_currency",
                "label": "Item after cost",
                'read_only' : 1
            },
             {
                "fieldname": "item_cost_value",
                "fieldtype": "Data",
                "insert_after": "item_after_cost",
                "label": "Item cost value",
                'read_only' : 1
            },
             {
                "fieldname": "purchase_currency",
                "fieldtype": "Data",
                "insert_after": "item_cost_value",
                "label": "Purchase Currency",
                'read_only' : 1
            },
        ] 
        } 
    
    
    }