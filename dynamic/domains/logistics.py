from frappe import _ 


data = {
    'custom_fields': {
        'Purchase Order': [
            {
                "label": _("Has Shipped"),
                "fieldname": "has_shipped",
                "fieldtype": "Check",
                "insert_after": "tax_withholding_category",
                "read_only" : 1
            },
            {
                "label": _("Has Delivered"),
                "fieldname": "has_delivered",
                "fieldtype": "Check",
                "insert_after": "has_shipped",
                "read_only" : 1
            },
        ],
        'Serial No':[
            {
                "label": _("Customer 2"),
                "fieldname": "customer_2",
                "fieldtype": "Link",
                "insert_after": "work_order",
                "options":"Customer",
            },
            {
                "label": _("Contact"),
                "fieldname": "contact",
                "fieldtype": "Link",
                "insert_after": "customer_2",
                "options":"Contact",
            },
        ],
        'Stock Entry': [
            {
                "label": _("Request Editing Item"),
                "fieldname": "request_editing_item",
                "fieldtype": "Link",
                "insert_after": "purchase_receipt_no",
                "options":"Request Editing Item",
                "read_only" : 1
            },
            
        ],
        'Customer': [
            {
                "label": _("Support"),
                "fieldname": "support",
                "fieldtype": "Check",
                "insert_after": "primary_address",
            },
            {
                "label": _("Location"),
                "fieldname": "location",
                "fieldtype": "Link",
                "insert_after": "support",
                "options":"Location"
            },
        ],
        'Sales Order Item': [
            {
                "label": "Serial Number",
                "fieldname": "serial_number",
                "fieldtype": "Link",
                "options":"Serial No",
                "insert_after": "item_code",
                "in_list_view": "1",
                "columns":1
            },
        ],
        'Purchase Order Item': [
            {
                "label": "Shipped qty",
                "fieldname": "shipped_qty",
                "fieldtype": "Float",
                'default' : '0' ,
                "insert_after": "item_code",
                "in_list_view": "1",
                "columns":1
            },
        ],
        # 'Lead': [
        #     {
        #         "fieldname": "logistic_column",
        #         "fieldtype": "Column Break",
        #         "insert_after": "fax",
        #         "label": "",
        #     },
        #     {
        #         "label": _("Phone 1"),
        #         "fieldname": "phone_number_1",
        #         "fieldtype": "Data",
        #         "insert_after": "website",
        #     },
        #     {
        #         "label": _("Phone 2"),
        #         "fieldname": "phone_number_2",
        #         "fieldtype": "Data",
        #         "insert_after": "phone_number_1",
        #     },
        # ],
        'Selling Settings': [
            {
                "fieldname": "quotation_settings",
                "fieldtype": "Section Break",
                "insert_after": "close_opportunity_after_days",
                "label": _("Quotation Settings"),
            },
            {
                "label": _("Default Mode of Payment Quotation"),
                "fieldname": "default_mode_of_payment_quotation",
                "fieldtype": "Link",
                "insert_after": "quotation_settings",
                "options":"Mode of Payment"
            },
            {
                "label": _("Diable Order Without Quotation"),
                "fieldname": "diable_order_without_quotation",
                "fieldtype": "Check",
                "insert_after": "default_mode_of_payment_quotation",
            },
            {
                "fieldname": "maintenance_settings",
                "fieldtype": "Section Break",
                "insert_after": "diable_order_without_quotation",
                "label": _("Maintenance Settings"),
            },
            {
                "label": _("Item Group"),
                "fieldname": "item_group",
                "fieldtype": "Link",
                "insert_after": "maintenance_settings",
                "options":"Item Group"
            },
            {
                "label": _("Price List"),
                "fieldname": "price_list",
                "fieldtype": "Link",
                "insert_after": "item_group",
                "options":"Price List"
            },
            {
                "fieldname": "maintenance_settings_column",
                "fieldtype": "Column Break",
                "insert_after": "price_list",
                "label": "",
            },
            {
                "label": _("Department"),
                "fieldname": "department",
                "fieldtype": "Link",
                "insert_after": "price_list",
                "options":"Department"
            },
            {
                "label": _("Account"),
                "fieldname": "account",
                "fieldtype": "Link",
                "insert_after": "department",
                "options":"Account"
            }
        ],
        'Quotation' :[
             {
                "fieldname": "material_reuqest",
                "fieldtype": "Link",
                "insert_after": "customer_name",
                "label": _("Material Request"),
                "options" : "Material Request" , 
                "read_only" : 0,
                "allow_on_submit":0,      
            },
            {
                "fieldname": "advance_paid",
                "fieldtype": "Currency",
                "insert_after": "in_words",
                "label": _("Advance Paid"),
                'options' : 'party_account_currency',
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "party_account_currency",
                "fieldtype": "Link",
                "insert_after": "advance_paid",
                "label": _("Party Account Currency"),
                'options' : 'Currency',
                'hidden' : 1 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "outstand_amount",
                "fieldtype": "Float",
                "insert_after": "source",
                "label": _("Outstand Amount"),
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "advance_payments",
                "fieldtype": "Section Break",
                "insert_after": "terms",
                "label": _("Advance Payments"),
            },
            {
                "fieldname": "allocate_advances_automatically",
                "fieldtype": "Check",
                "insert_after": "advance_payments",
                "label": _("Allocate Advances Automatically (FIFO)"),
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 0 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 0 ,
            },
            {
                "fieldname": "get_advances",
                "fieldtype": "Button",
                "insert_after": "allocate_advances_automatically",
                "label": _("Get Advances Received"),
                'hidden' : 0 ,
                'read_only' : 0 ,
                'no_copy' : 0 ,
                'allow_on_submit' : 0 ,
            },
            {
                "fieldname": "advances",
                "fieldtype": "Table",
                "insert_after": "get_advances",
                "options":"Sales Invoice Advance",
                "label": _("Advances"),
                'hidden' : 0 ,
                'read_only' : 0 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 0 ,
            },
            {
                "fieldname": "base_write_off_amount",
                "fieldtype": "Currency",
                "insert_after": "base_rounded_total",
                "options":"Company:company:default_currency",
                "label": _("Write Off Amount (Company Currency)"),
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "total_advance",
                "fieldtype": "Currency",
                "insert_after": "rounded_total",
                "options":"party_account_currency",
                "label": _("Total Advance"),
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "write_off_amount",
                "fieldtype": "Currency",
                "insert_after": "total_advance",
                "options":"currency",
                "label": _("Write Off Amount"),
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "is_return",
                "fieldtype": "Check",
                "insert_after": "write_off_amount",
                "options":"currency",
                "label": _("is Return"),
                'default' : '0' ,
                'hidden' : 1 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },

            {
                "fieldname": "outstanding_amount",
                "fieldtype": "Float",
                "insert_after": "is_return",
                "label": _("Outstanding Amount"),
                "read_only" : 1,
                "no_copy" : 1,
                "allow_on_submit":1,
                "default":0
            },
            {
                "label": _("Cost Center"),
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "insert_after": "order_type",
                "options" : "Cost Center" , 
                "read_only" : 0,
                "allow_on_submit":0,
                "reqd":1
                
            },
            
            
        ],
         "Sales Order":[
            {
                "label": _("Valid Until"),
                "fieldname": "valid_until",
                "fieldtype": "Date",
                "insert_after": "order_type",
                "read_only" : 1,
            },
            {
                "label": _("Update Validation Date"),
                "fieldname": "update_validation_date",
                "fieldtype": "Check",
                "insert_after": "valid_until",
            },
            {
                "label": _("Survey"),
                "fieldname": "survey",
                "fieldtype": "Data",
                "insert_after": "update_validation_date",
            },
            # {
            #     "label": "Advance Payment",
            #     "fieldname": "advance_paymentss",
            #     "fieldtype": "Section Break",
            #     "insert_after": "payment_schedule"
            # },
            # {
            #     "label": "Get Advances Receivedd",
            #     "fieldname": "get_advancess",
            #     "fieldtype": "Button",
            #     "insert_after": "advance_paymentss",
            #     "allow_on_submit":1
            # },
            # {
            #     "label": "Advances",
            #     "fieldname": "advancess",
            #     "fieldtype": "Table",
            #     "options":"Sales Invoice Advance",
            #     "insert_after": "get_advancess",
            #     "allow_on_submit":1
            # },
            # {
            #     "label": _("Outstanding Amount"),
            #     "fieldname": "outstanding_amount",
            #     "fieldtype": "Float",
            #     "insert_after": "advance_paid",
            #     "allow_on_submit":1,
            #     "read_only" : 1
            # },
                         
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
            {
                "label": "Customer Print Name",
                "fieldname": "customer_print_name",
                "fieldtype": "Data",
                "insert_after": "order_type",
                "allow_on_submit": "1",
            },
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
            {
                "fieldname": "advance_payments",
                "fieldtype": "Section Break",
                "insert_after": "terms",
                "label": "Advance Payments",
            },
            {
                "fieldname": "allocate_advances_automatically",
                "fieldtype": "Check",
                "insert_after": "advance_payments",
                "label": "Allocate Advances Automatically (FIFO)",
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 0 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 0 ,
            },
            {
                "fieldname": "get_advances",
                "fieldtype": "Button",
                "insert_after": "allocate_advances_automatically",
                "label": "Get Advances Received",
                'hidden' : 0 ,
                'read_only' : 0 ,
                'no_copy' : 0 ,
                'allow_on_submit' : 0 ,
            },
            {
                "fieldname": "advances",
                "fieldtype": "Table",
                "insert_after": "get_advances",
                "options":"Sales Invoice Advance",
                "label": "Advances",
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 0 ,
            },
            {
                "fieldname": "base_write_off_amount",
                "fieldtype": "Currency",
                "insert_after": "base_rounded_total",
                "options":"Company:company:default_currency",
                "label": "Write Off Amount (Company Currency)",
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "total_advance",
                "fieldtype": "Currency",
                "insert_after": "rounded_total",
                "options":"party_account_currency",
                "label": "Total Advance",
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "write_off_amount",
                "fieldtype": "Currency",
                "insert_after": "total_advance",
                "options":"currency",
                "label": "Write Off Amount",
                'default' : '0' ,
                'hidden' : 0 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
            {
                "fieldname": "is_return",
                "fieldtype": "Check",
                "insert_after": "write_off_amount",
                "options":"currency",
                "label": "is Return",
                'default' : '0' ,
                'hidden' : 1 ,
                'read_only' : 1 ,
                'no_copy' : 1 ,
                'allow_on_submit' : 1 ,
            },
             {
                "fieldname": "opportunity",
                "fieldtype": "Link",
                "insert_after": "source",
                "label": "Opportunity",
                'options' : 'Opportunity' ,
            },  
        ],
    }

}