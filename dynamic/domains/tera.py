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
        ],
        'Company':[
            {
                "fieldname": "sales_return_account",
                "fieldtype": "Link",
                "options":"Account",
                "insert_after": "unrealized_profit_loss_account",
                "label": "Sales Return Account"
            },
        ],
        'Item Group':[
            {
                "fieldname": "code",
                "fieldtype": "Data",
                "insert_after": "column_break_5",
                "label": "Group Code",
                "unique": 1,
                "reqd":1

            },
        ] 



    },
    "properties": [

    ],
    "property_setters": [
        # {
        #     "doc_type": "Item",
        #     "doctype_or_field": "DocType",
        #     "name": "Item-main-autoname",
        #     "property": "autoname",
        #     "property_type": "Data",
        #     "value": "field:item_name"
        #     }

    ],
    'on_setup': 'dynamic.terra.setup.create_terra_scripts'
}