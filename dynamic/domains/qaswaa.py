
from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        "Sales Order":
        [ 
            {
                "label": "Notes",
                "fieldname": "notes",
                "fieldtype": "Small Text",
                "insert_after": "to_date" ,
            },
        ],
        "Quotation":
        [ 
           
            {
                "label": "Sales Team",
                "fieldname": "sales_team_section_break_",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule" ,
            },
            {
                "label": "Sales Team Qt",
                "fieldname": "sales_team_qt",
                "fieldtype": "Table",
                "insert_after": "sales_team_section_break_" ,
                "options":"Sales Team",
            },
            {
                "label": "Notes",
                "fieldname": "notes",
                "fieldtype": "Small Text",
                "insert_after": "source" ,
            },
        
        ],
        "Quotation Item":
        [ 
           
            {
                "label": "Item Name Print",
                "fieldname": "item_name_print",
                "fieldtype": "Data",
                "insert_after": "item_name" ,
            },
        ],
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
            {
                "label": "Notes",
                "fieldname": "notes",
                "fieldtype": "Small Text",
                "insert_after": "to_date" ,
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