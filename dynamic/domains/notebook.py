

#notebook_no
from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Journal Entry':[
            {
                "label":_("Notebook No"),
                "fieldname":"notebook_no",
                "fieldtype":"Data",
                "insert_after":"multi_currency", 
            },
        ],
        'Payment Entry':[
            {
                "label":_("Notebook No"),
                "fieldname":"notebook_no",
                "fieldtype":"Data",
                "insert_after":"remarks", 
            },
        ],
    }
}

