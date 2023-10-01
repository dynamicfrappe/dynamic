

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Quotation':[
            {
                "label":_("Project"),
                "fieldname":"project",
                "fieldtype":"Link",
                "options":"Project",
                "insert_after":"items_section", 
                "no_copy":1, 
            },
            {
                "label":_(""),
                "fieldname":"card_items_sect",
                "fieldtype":"Section Break",
                "insert_after":"total_net_weight", 
                "no_copy":1, 
            },
            {
                "label":_("Card Items"),
                "fieldname":"card_items",
                "fieldtype":"Table",
                "options":"Comparison Item Card Stock Item",
                "insert_after":"card_items_sect", 
                "no_copy":1, 
            },
            {
                "label":_("Card Services"),
                "fieldname":"card_services",
                "fieldtype":"Table",
                "options":"Comparison Item Card Service Item",
                "insert_after":"card_items", 
                "no_copy":1, 
            },
            
        ],
        
    },
      "properties": [
        
    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}







