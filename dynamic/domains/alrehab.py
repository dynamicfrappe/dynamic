from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    'custom_fields': {
        'Customer':[
            {
                "label":_("Owner Name"),
                "fieldname":"owner_name",
                "fieldtype":"Link",
                "options":"Owner",
                "insert_after":"customer_type",  
            },   
            {
                "label":_("Commercial year"),
                "fieldname":"commercial_year",
                "fieldtype":"Link",
                "options":"Commercial year",
                "insert_after":"owner_name",  
            },     
            #Unit area
            {
                "label":_("Unit area"),
                "fieldname":"unit_area",
                "fieldtype":"Data",
                "insert_after":"commercial_year",  
            },  
            {
                 "label":_("Building Number"),
                "fieldname":"building_number",
                "fieldtype":"Data",
                "insert_after":"unit_area", 

            }

        ],
        'Journal Entry':[
            {
                "label":_("installment Entry"),
                "fieldname":"installment_entry",
                "fieldtype":"Link",
                "options":"installment Entry",
                "insert_after":"tax_withholding_category", 
            }
        ]
        
        
    },
    "properties": [
        {
        "doctype": "Journal Entry",
        "doctype_or_field": "DocField",
        "fieldname": "installment_entry",
        "property": "read_only",
        "property_type": "Check",
        "value": "1",
        },
    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}