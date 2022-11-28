from __future__ import unicode_literals


data = {

    'custom_fields': {
         'Sales Order':[
            # {
            #     "fieldname": "reservation",
            #     "fieldtype": "Link",
            #     "insert_after": "project",
            #     "label": "Reservation",
            #     'options' : 'Reservation',
            #     'read_only' : 1
            # },
            {
                "fieldname": "purchase_order",
                "fieldtype": "Link",
                "insert_after": "set_warehouse",
                "label": "Purchase Order",
                'options' : 'Purchase Order'
            },
            {
                "fieldname": "reservation_status",
                "fieldtype": "Select",
                "options": "\nActive\nClosed\nInvalid",
                "insert_after": "set_warehouse",
                "label": "Reservation Status",
                'read_only' : 1,
                "fetch_from": "reservation.status",
                "allow_on_submit":1 
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
            # "unique": 1,
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
            },
            {
                "fieldname": "reservation_setting_section",
                "fieldtype": "Section Break",
                "insert_after": "email_setting"
            },
            {
                "fieldname": "reservation_setting",
                "fieldtype": "Table",
                "options":"Reservation Child",
                "insert_after": "reservation_setting_section",
                "label": "Reservation Setting",
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
        'Sales Order Item':[
             {
            "fieldname": "reservation",
            "fieldtype": "Link",
            "options": "Reservation",
            "insert_after": "section_break_5",
            "label": "Reservation",
            # "in_list_view":1,
            "allow_on_submit":1,
            "read_only" : 1,
            "no_copy":1
            },
            {
            "fieldname": "reservation_status",
            "fieldtype": "Data",
            "insert_after": "reservation",
            "label": "Reservation Status",
            # "in_list_view":1,
            "allow_on_submit":1,
            "read_only" : 1,
            "no_copy":1
            },
            {
            "fieldname": "item_warehouse",
            "fieldtype": "Link",
            "insert_after": "item_name",
            "label": "Item Warehouse",
            'options' : 'Warehouse'
            # "in_list_view":1,
            },
            {
            "fieldname": "item_purchase_order",
            "fieldtype": "Link",
            "insert_after": "item_warehouse",
            "label": "Purchase Order",
            'options' : 'Purchase Order'
            # "in_list_view":1,
            },
            {
            "fieldname": "schedule_date",
            "fieldtype": "Date",
            "insert_after": "item_purchase_order",
            "label": "Required By",
            'options' : 'Purchase Order',
            'fetch_from':'item_purchase_order.schedule_date',
            "read_only" : 1,
            "fetch_if_empty": 1
            },
            {
                "fieldname": "sub_uom",
                "fieldtype": "Link",
                "insert_after": "picked_qty",
                "label": "Sub Uom",
                "options" : 'UOM',
                "read_only":1,
            
            },
            {
                "fieldname": "sub_uom_conversation_factor",
                "fieldtype": "Float",
                "insert_after": "sub_uom",
                "label": "Sub Uom Conversion Factor",
                "read_only":1
            },
            {
                "fieldname": "qty_as_per_sub_uom",
                "fieldtype": "Float",
                "insert_after": "sub_uom_conversation_factor",
                "label": "QTY As Per Sub Uom",
                "read_only":1
            
            }
        ], 
        "Sales Order":[
             {
                "fieldname": "invoice_payment",
                "fieldtype": "Float",
                "insert_after": "advance_paid",
                "label": "Invoice Payment",
                "read_only" : 1,
                "no_copy" : 1,
                "allow_on_submit":1,
                "default":0
            },
            {
                "fieldname": "outstanding_amount",
                "fieldtype": "Float",
                "insert_after": "invoice_payment",
                "label": "Outstanding Amount",
                "read_only" : 1,
                "no_copy" : 1,
                "allow_on_submit":1,
                "default":0
            },
        ],
        "Purchase Order Item":[
             {
                "fieldname": "sub_uom",
                "fieldtype": "Link",
                "insert_after": "stock_uom",
                "label": "Sub Uom",
                "options" : 'UOM',
                "read_only":1,
            
            },
            {
                "fieldname": "sub_uom_conversation_factor",
                "fieldtype": "Float",
                "insert_after": "sub_uom",
                "label": "Sub Uom Conversion Factor",
                "read_only":1
            },
            {
                "fieldname": "qty_as_per_sub_uom",
                "fieldtype": "Float",
                "insert_after": "sub_uom_conversation_factor",
                "label": "QTY As Per Sub Uom",
                "read_only":1
            
            }
        ],
        "Delivery Note Item":[
             {
                "fieldname": "sub_uom",
                "fieldtype": "Link",
                "insert_after": "stock_uom",
                "label": "Sub Uom",
                "options" : 'UOM',
                "read_only":1,
            
            },
            {
                "fieldname": "sub_uom_conversation_factor",
                "fieldtype": "Float",
                "insert_after": "sub_uom",
                "label": "Sub Uom Conversion Factor",
                "read_only":1
            },
            {
                "fieldname": "qty_as_per_sub_uom",
                "fieldtype": "Float",
                "insert_after": "sub_uom_conversation_factor",
                "label": "QTY As Per Sub Uom",
                "read_only":1
            
            }
        ],
        #New Request Update 1- Update Cost Center Warehouse
        "Cost Center" :[
            {
                    "fieldname": "payment_naming",
                    "fieldtype": "Data",
                    "insert_after": "old_parent",
                    "label": "Branch Options"   

            },
            {
                    "fieldname": "branch_section",
                    "fieldtype": "Section Break",
                    "insert_after": "old_parent",
                    "label": "Branch Options"   

            },
            
             {
                "fieldname": "warehouse",
                "fieldtype": "Link",
                "insert_after": "intermediate_warehouse",
                "label": "Warehouse",
                'options' : 'Warehouse'
            
            },
              {
                "fieldname": "manager",
                "fieldtype": "Table",
                "insert_after": "warehouse",
                "label": "Branch managers",
                'options' : 'Branch Managers'
            
            },

        ] ,
        "Quotation Item":[
            {
                "fieldname": "sub_uom",
                "fieldtype": "Link",
                "insert_after": "stock_uom",
                "label": "Sub Uom",
                "options" : 'UOM',
                "read_only":1,
            
            },
            {
                "fieldname": "sub_uom_conversation_factor",
                "fieldtype": "Float",
                "insert_after": "sub_uom",
                "label": "Sub Uom Conversion Factor",
                "read_only":1
            },
            {
                "fieldname": "qty_as_per_sub_uom",
                "fieldtype": "Float",
                "insert_after": "sub_uom_conversation_factor",
                "label": "QTY As Per Sub Uom",
                "read_only":1
            
            }
        ],
        "Stock Entry Detail":[
            {
                "fieldname": "sub_uom",
                "fieldtype": "Link",
                "insert_after": "transfer_qty",
                "label": "Sub Uom",
                "options" : 'UOM',
                "read_only":1,
            
            },
            {
                "fieldname": "sub_uom_conversation_factor",
                "fieldtype": "Float",
                "insert_after": "sub_uom",
                "label": "Sub Uom Conversion Factor",
                "read_only":1
            },
            {
                "fieldname": "qty_as_per_sub_uom",
                "fieldtype": "Float",
                "insert_after": "sub_uom_conversation_factor",
                "label": "QTY As Per Sub Uom",
                "read_only":1
            
            }
        ],
         "Purchase Receipt Item":[
            {
                "fieldname": "sub_uom",
                "fieldtype": "Link",
                "insert_after": "stock_qty",
                "label": "Sub Uom",
                "options" : 'UOM',
                "read_only":1,
            
            },
            {
                "fieldname": "sub_uom_conversation_factor",
                "fieldtype": "Float",
                "insert_after": "sub_uom",
                "label": "Sub Uom Conversion Factor",
                "read_only":1
            },
            {
                "fieldname": "qty_as_per_sub_uom",
                "fieldtype": "Float",
                "insert_after": "sub_uom_conversation_factor",
                "label": "Recived QTY As Per Sub Uom",
                "read_only":1
            
            }
        ],
        "UOM Conversion Detail":[
            {
                "fieldname": "is_sub_uom",
                "fieldtype": "Check",
                "insert_after": "conversation_factor",
                "label": "Is Sub Uom",
                "in_list_view":1
            
            }
        ]



    },
    # "properties": [
        
    # ],
    "properties": [
        {
        "doctype": "Item",
        "doctype_or_field": "DocField",
        "fieldname": "item_code",
        "property": "read_only",
        "property_type": "Check",
        "value": "1"
        },
         {
        "doctype": "Sales Order",
        "doctype_or_field": "DocField",
        "fieldname": "set_warehouse",
        "property": "reqd",
        "property_type": "Check",
        "value": "0"
        },
        {
        "doctype": "Sales Order Item",
        "doctype_or_field": "DocField",
        "fieldname": "warehouse",
        "property": "read_only",
        "property_type": "Check",
        "value": "0"
        },
    ],
  
    'on_setup': 'dynamic.terra.setup.create_terra_scripts'
}