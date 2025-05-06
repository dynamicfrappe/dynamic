from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
                'Payment Term':[
            {
                "label":_("Disable on"),
                "fieldname":"disable_on",
                "fieldtype":"Date",
                "insert_after":"credit_days", 
            },
                {
                "label":_("Is able"),
                "fieldname":"is_usable",
                "fieldtype": "Check",
                "insert_after":"disable_on",
            },
                ],
            'Pricing Rule Item Code':[
                {
                "label":_("Unit area"),
                "fieldname":"unit_area1",
                "fieldtype":"Data",
                "insert_after":"uom", 
            },
                {
                "label":_("Unit Floor"),
                "fieldname":"unit_floor",
                "fieldtype": "Data",
                "insert_after":"unit_area",
            },        
            ]
    },
    "properties": [
        
    ],
}