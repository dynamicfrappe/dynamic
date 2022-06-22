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
                "insert_after": "items",
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
        'Landed Cost Taxes and Charges':[
             {
                "fieldname": "line_name",
                "fieldtype": "Data",
                "insert_after": "base_amount",
                "label": "Line Name",
                "read_only" : 1
               

            },
             {
                "fieldname": "docment_type",
                "fieldtype": "Data",
                "insert_after": "line_name",
                "label": "Document Type",
                "read_only" : 1
               

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
        ],
        'Lead':[
             {
                "fieldname": "phone_no",
                "fieldtype": "Data",
                "in_global_search": 1,
                "in_standard_filter": 1,
                "insert_after": "email_id",
                "label": "Phone No",
                "translatable": 1,
                "unique": 1,
            },
            
        ] ,
        'Customer':[
             {
            "fieldname": "phone_no",
            "fieldtype": "Data",
            "in_global_search": 1,
            "in_standard_filter": 1,
            "insert_after": "tax_category",
            "label": "Phone No",
            "translatable": 1,
            "unique": 1,
            "fetch_if_empty": 1,
            "fetch_from": "lead_name.phone_no", 
            },
             {
                "fieldname": "from_opportunity",
                "fieldtype": "Link",
                "insert_after": "from_lead",
                "label": "From Opportunity",
                "options":"Opportunity"
            }
        ],
        'Opportunity':[
             {
            "fieldname": "phone_no",
            "fieldtype": "Data",
            "in_global_search": 1,
            "in_standard_filter": 1,
            "insert_after": "source",
            "label": "Phone No",
            "translatable": 1,
            "unique": 1,
            "fetch_if_empty": 1,
            "fetch_from": "party_name.phone_no" 
            },
             {
            "fieldname": "opportunity_name",
            "fieldtype": "Data",
            "insert_after": "naming_series",
            "label": "Opportunity Name",
            "translatable": 1,
            }
        ],
        'Stock Settings':[
            {
                "fieldname": "email_section",
                "fieldtype": "Section Break",
                "insert_after": "stock_auth_role"
            },
            {
            "fieldname": "email_setting",
            "fieldtype": "Table",
            "options":"Email Setting",
            "insert_after": "email_section",
            "label": "Email Setting",
            "translatable": 1,
            }
        ] 
    },
    "properties": [
        
    ],
    "property_setters": [
        # {
        # "doc_type": "Lead",
        # "doctype_or_field": "DocType",
        # "name": "Lead-main-search_fields",
        # "property": "search_fields",
        # "property_type": "Data",
        # "value": "lead_name,lead_owner,phone_no"
        # }
        ],
  
    'on_setup': 'dynamic.terra.setup.create_terra_scripts'
}