from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    'custom_fields': {
        'Downtime Entry':[
           {             
                "label":_("Cost"),
                "fieldname":"cost",
                "fieldtype":"Currency",
                "insert_after":"column_break_4", 
                
            },

        ],
  
        'Workstation':[
            {
                "fieldname":_("Minimun Quantity"),
                "fieldname":"min_qty",
                "fieldtype":"Float",
                "insert_after":"production_capacity",               
            },
           
        ],
       
        
    },
 
}