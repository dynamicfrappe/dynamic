from __future__ import unicode_literals
from frappe import _ 

data = {
    'custom_fields': {
        'Sales Invoice Item': [
            {
                "label": _("Date"),
                "fieldname": "date_1",
                "fieldtype": "Date",
                "insert_after": "item_code",
            },
            {
                "label": _("Work Number"),
                "fieldname": "work_number",
                "fieldtype": "Data",
                "insert_after": "date_1",
            },
        ],
    }

}