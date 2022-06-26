from __future__ import unicode_literals


data = {

    'custom_fields': {
         'Sales Order':[
            {
                "fieldname": "reservation",
                "fieldtype": "Link",
                "insert_after": "project",
                "label": "Reservation",
                'options' : 'Reservation',
                'read_only' : 1
            },
         ],
         'Landed Cost Item': [
            {
                "fieldname": "rate_currency",
                "fieldtype": "Currency",
                "insert_after": "rate",
                "label": "Price in supplier currency",
                'read_only' : 1
            },
               {
                "fieldname": "item_after_cost",
                "fieldtype": "Currency",
                "insert_after": "rate_currency",
                "label": "Item after cost in company Currency",
                'read_only' : 1
            },
             {
                "fieldname": "item_cost_value",
                "fieldtype": "Currency",
                "insert_after": "item_after_cost",
                "label": "Item cost value in Company Currency",
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
                "label": "Invocie Currency Factor",
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
                "fieldtype": "Currency",
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
             {
                "fieldname": "docment_name",
                "fieldtype": "Data",
                "insert_after": "docment_type",
                "label": "Document Name",
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
            "reqd": 1
            }
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
            "reqd": 1
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
            "reqd": 1,
            "fetch_from": "party_name.phone_no" 
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
        ],
        'Material Request':[
             {
            "fieldname": "project_name",
            "fieldtype": "Link",
            "options": "Project Name",
            "insert_after": "material_request_type",
            "label": "Project Name"
            }
        ],  
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
         {
        "doc_type": "Sales Order",
        "doctype_or_field": "DocField",
        "field_name": "set_warehouse",
        "property": "reqd",
        "property_type": "Check",
        "value": "1"
        },

    ],
  
    'on_setup': 'dynamic.terra.setup.create_terra_scripts'
}