import frappe
from frappe import _

data = {
    'custom_fields': {
        'Opportunity': [
            {
                "label": "Sales Person",
                "fieldname": "sales_person",
                "fieldtype": "Link",
                'options' : 'Sales Person' ,
                "insert_after": "contact_date",
                "in_standard_filter": "1",
            },
        ],
        'Lead': [
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "email_id",
                "options":"Sales Person"
            },
        ],
    }

}