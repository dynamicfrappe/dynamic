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
             {
                "fieldname": "currency",
                "fieldtype": "Data",
                "insert_after": "item_cost_valu",
                "label": "Currency",
                'read_only' : 1
            },
        ],
         "Landed Cost Voucher" :[
            {
                "fieldname": "cost_set_section",
                "fieldtype": "Section Break",
                "insert_after": "taxes",
                "label": "Cost Section",
               
            },
             {
                "fieldname": "cost_child_table",
                "fieldtype": "Table",
                "insert_after": "cost_set_section",
                "label": "Charges",
                "options" :"Landed Cost Voucher Child"
            },


        ] ,
        
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
        {
        "doc_type": "Item",
        "doctype_or_field": "DocField",
        "field_name": "item_code",
        "property": "read_only",
        "property_type": "Check",
        "value": "1"
        },

    ],
  
    'on_setup': 'dynamic.terra.setup.create_terra_scripts'
}