from __future__ import unicode_literals
from frappe import _ 

data = {
    'custom_fields': {
        'Sales Invoice': [
            {
                "label": _("Contract Number"),
                "fieldname": "contract_number",
                "fieldtype": "Date",
                "insert_after": "naming_series",
            },
            {
                "label": _("Deduction"),
                "fieldname": "deduction",
                "fieldtype": "Float",
                "insert_after": "contract_number",
            },
            {
                "label": _("Abstract Number"),
                "fieldname": "abstract_number",
                "fieldtype": "Data",
                "insert_after": "deduction",
            },
        ],
    }

}