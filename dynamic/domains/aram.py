

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
            
        ],
        
    },
      "properties": [
        
    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}







