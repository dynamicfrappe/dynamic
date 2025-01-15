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
    }
}