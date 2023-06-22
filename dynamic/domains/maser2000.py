
from __future__ import unicode_literals

data = {
'custom_fields': {
        'Stock Entry': [
            {
                "label": "Cost Center",
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "options":"Cost Center",
                "insert_after": "stock_entry_type",
            },
            {
                "label": "Permission Number",
                "fieldname": "permission_number",
                "fieldtype": "Data",
                "insert_after": "cost_center",
            },
        ],
        'Pay Document': [
            {
                "label": "",
                "fieldname": "col_break_rf_num",
                "fieldtype": "Column Break",
                "insert_after": "notes",
            },
            {
                "label": "Reference Number",
                "fieldname": "reference_number",
                "fieldtype": "Data",
                "insert_after": "col_break_rf_num",
            },
        ],
        'Receipt Document': [
            {
                "label": "",
                "fieldname": "col_break_rf_num",
                "fieldtype": "Column Break",
                "insert_after": "notes",
            },
            {
                "label": "Reference Number",
                "fieldname": "reference_number",
                "fieldtype": "Data",
                "insert_after": "col_break_rf_num",
            },
        ],
}
}