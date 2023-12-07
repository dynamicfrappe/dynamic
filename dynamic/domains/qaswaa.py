
from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        "Item Group":
        [ 
           
            {
                "label": "Group Code",
                "fieldname": "group_code",
                "fieldtype": "Data",
                "insert_after": "column_break_5" ,
            },
        
        ],
        "Sales Invoice":
        [ 
           
            {
                "label": "Customer Name.",
                "fieldname": "customer_name_hand",
                "fieldtype": "Data",
                "insert_after": "customer_name" ,
            },
        
        ],
        "Selling Settings":
        [
            {
                "label": "Apply Reservation",
                "fieldname": "apply_reservation",
                "fieldtype": "Check",
                "insert_after": "territory" ,
            },
        ]
    },
     "properties": [
        {
        # "doctype": "Sales Invoice",
        # "doctype_or_field": "DocField",
        # "fieldname": "customer_name",
        # "property": "read_only",
        # "property_type": "Check",
        # "value": "0"
        },
     ]
}