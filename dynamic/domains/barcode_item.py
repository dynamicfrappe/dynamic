

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Item Barcode':[
            {
                "label":_("Item Barcode"),
                "fieldname":"item_barcode",
                "fieldtype":"Barcode",
                "insert_after":"barcode", 
            },
        ],
        
    },
      "properties": [

    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}







