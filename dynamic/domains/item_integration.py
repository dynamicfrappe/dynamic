import frappe
from frappe import _ 


data = {
    'custom_fields': {
        'Stock Settings': [
            {
                "label": _("Item Itegration"),
                "fieldname": "section_break_item_inegration",
                "fieldtype": "Section Break",
                "insert_after": "reorder_email_notify",
            },
            {
                "label": _("Enable"),
                "fieldname": "enable_item_itegration",
                "fieldtype": "Check",
                "insert_after": "section_break_item_inegration",
            },
            {
                "label": _("URL"),
                "fieldname": "url_item_integration",
                "fieldtype": "Data",
                "insert_after": "enable_item_itegration",
            },
            {
                "label": _("Token"),
                "fieldname": "token_item_integration",
                "fieldtype": "Data",
                "insert_after": "url_item_integration",
            },
        ],
    }

}