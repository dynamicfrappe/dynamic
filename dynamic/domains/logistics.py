from frappe import _ 


data = {
    'custom_fields': {
        # 'Purchase Order': [
        #     {
        #         "label": _("Has Shipped"),
        #         "fieldname": "has_shipped",
        #         "fieldtype": "Check",
        #         "insert_after": "tax_withholding_category",
        #         "read_only" : 1
        #     },
        # ],
        # 'Customer': [
        #     {
        #         "label": _("Support"),
        #         "fieldname": "support",
        #         "fieldtype": "Check",
        #         "insert_after": "primary_address",
        #     },
        #     {
        #         "label": _("Location"),
        #         "fieldname": "location",
        #         "fieldtype": "Link",
        #         "insert_after": "support",
        #         "options":"Location"
        #     },
        # ],
        # 'Selling Settings': [
        #     {
        #         "fieldname": "quotation_settings",
        #         "fieldtype": "Section Break",
        #         "insert_after": "close_opportunity_after_days",
        #         "label": _("Quotation Settings"),
        #     },
        #     {
        #         "label": _("Default Mode of Payment Quotation"),
        #         "fieldname": "default_mode_of_payment_quotation",
        #         "fieldtype": "Link",
        #         "insert_after": "quotation_settings",
        #         "options":"Mode of Payment"
        #     },
        #     {
        #         "label": _("Diable Order Without Quotation"),
        #         "fieldname": "diable_order_without_quotation",
        #         "fieldtype": "Check",
        #         "insert_after": "default_mode_of_payment_quotation",
        #     },
        #     {
        #         "fieldname": "maintenance_settings",
        #         "fieldtype": "Section Break",
        #         "insert_after": "diable_order_without_quotation",
        #         "label": _("Maintenance Settings"),
        #     },
        #     {
        #         "label": _("Item Group"),
        #         "fieldname": "item_group",
        #         "fieldtype": "Link",
        #         "insert_after": "maintenance_settings",
        #         "options":"Item Group"
        #     },
        #     {
        #         "label": _("Price List"),
        #         "fieldname": "price_list",
        #         "fieldtype": "Link",
        #         "insert_after": "item_group",
        #         "options":"Price List"
        #     },
        #     {
        #         "label": _("Department"),
        #         "fieldname": "department",
        #         "fieldtype": "Link",
        #         "insert_after": "price_list",
        #         "options":"Department"
        #     }
        # ],
        
        'Quotation' :[
             {
                "label": _("Material Request"),
                "fieldname": "material_reuqest",
                "fieldtype": "Link",
                "insert_after": "customer_name",
                "options" : "Material Request" , 
                "read_only" : 0,
                "allow_on_submit":0,      
            },
            # {
            #     "fieldname": "advance_paid",
            #     "fieldtype": "Currency",
            #     "insert_after": "in_words",
            #     "label": _("Advance Paid"),
            #     'options' : 'party_account_currency',
            #     'default' : '0' ,
            #     'hidden' : 0 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },
            # {
            #     "fieldname": "party_account_currency",
            #     "fieldtype": "Link",
            #     "insert_after": "advance_paid",
            #     "label": _("Party Account Currency"),
            #     'options' : 'Currency',
            #     'hidden' : 1 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },
            # {
            #     "fieldname": "outstand_amount",
            #     "fieldtype": "Float",
            #     "insert_after": "source",
            #     "label": _("Outstand Amount"),
            #     'hidden' : 0 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },
            # {
            #     "fieldname": "advance_payments",
            #     "fieldtype": "Section Break",
            #     "insert_after": "terms",
            #     "label": _("Advance Payments"),
            # },
            # {
            #     "fieldname": "allocate_advances_automatically",
            #     "fieldtype": "Check",
            #     "insert_after": "advance_payments",
            #     "label": _("Allocate Advances Automatically (FIFO)"),
            #     'default' : '0' ,
            #     'hidden' : 0 ,
            #     'read_only' : 0 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 0 ,
            # },
            # {
            #     "fieldname": "get_advances",
            #     "fieldtype": "Button",
            #     "insert_after": "allocate_advances_automatically",
            #     "label": _("Get Advances Received"),
            #     'hidden' : 0 ,
            #     'read_only' : 0 ,
            #     'no_copy' : 0 ,
            #     'allow_on_submit' : 0 ,
            # },
            # {
            #     "fieldname": "advances",
            #     "fieldtype": "Table",
            #     "insert_after": "get_advances",
            #     "options":"Sales Invoice Advance",
            #     "label": _("Advances"),
            #     'hidden' : 0 ,
            #     'read_only' : 0 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 0 ,
            # },
            # {
            #     "fieldname": "base_write_off_amount",
            #     "fieldtype": "Currency",
            #     "insert_after": "base_rounded_total",
            #     "options":"Company:company:default_currency",
            #     "label": _("Write Off Amount (Company Currency)"),
            #     'default' : '0' ,
            #     'hidden' : 0 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },
            # {
            #     "fieldname": "total_advance",
            #     "fieldtype": "Currency",
            #     "insert_after": "rounded_total",
            #     "options":"party_account_currency",
            #     "label": _("Total Advance"),
            #     'default' : '0' ,
            #     'hidden' : 0 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },
            # {
            #     "fieldname": "write_off_amount",
            #     "fieldtype": "Currency",
            #     "insert_after": "total_advance",
            #     "options":"currency",
            #     "label": _("Write Off Amount"),
            #     'default' : '0' ,
            #     'hidden' : 0 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },
            # {
            #     "fieldname": "is_return",
            #     "fieldtype": "Check",
            #     "insert_after": "write_off_amount",
            #     "options":"currency",
            #     "label": _("is Return"),
            #     'default' : '0' ,
            #     'hidden' : 1 ,
            #     'read_only' : 1 ,
            #     'no_copy' : 1 ,
            #     'allow_on_submit' : 1 ,
            # },

            # {
            #     "fieldname": "outstanding_amount",
            #     "fieldtype": "Float",
            #     "insert_after": "is_return",
            #     "label": _("Outstanding Amount"),
            #     "read_only" : 1,
            #     "no_copy" : 1,
            #     "allow_on_submit":1,
            #     "default":0
            # },
            # {
            #     "label": _("Cost Center"),
            #     "fieldname": "cost_center",
            #     "fieldtype": "Link",
            #     "insert_after": "order_type",
            #     "options" : "Cost Center" , 
            #     "read_only" : 0,
            #     "allow_on_submit":0,
            #     "reqd":1
                
            # },
            
            
        ],
    }

}