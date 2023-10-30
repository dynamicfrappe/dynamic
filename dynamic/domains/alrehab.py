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

        ],
        
        
    },
      "properties": [
        
    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}