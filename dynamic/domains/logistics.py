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
        ],
        'Selling Settings': [
            {
                "label": _("Default Mode of Payment Quotation"),
                "fieldname": "default_mode_of_payment_quotation",
                "fieldtype": "Link",
                "insert_after": "campaign_naming_by",
                "options":"Mode of Payment"
            },
        ],
    }

}