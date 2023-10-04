

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Quotation Item':[
            {
                "label": "Build",
                "fieldname": "build",
                "fieldtype": "Data",
                "insert_after": "ordered_qty",
            }
            
            
        ],
        'Comparison Item':[
            {
                "label": "Build",
                "fieldname": "build",
                "fieldtype": "Data",
                "insert_after": "remaining_purchased_qty",
            }
        ]
        
    },
      "properties": [
        
    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}







