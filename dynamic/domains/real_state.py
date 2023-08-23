

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Stock Entry':[
            {
                "label":_("Real State Cost"),
                "fieldname":"real_state_cost",
                "fieldtype":"Link",
                "options":"Real State Cost",
                "read_only":"1", 
                "insert_after":"total_amount", 
            },
        ],
        'Landed Cost Taxes and Charges':[
            {
                "label":_("Cost Center"),
                "fieldname":"taxes_cost_center",
                "fieldtype":"Link",
                "insert_after":"base_amount", 
                "options":"Cost Center", 
                "in_list_view":"1", 
            },
        ],
        'Item':[
            {
                "label":_("Unit Info"),
                "fieldname":"unit_info",
                "fieldtype":"Section Break",
                "insert_after":"image", 
            },
            {
                "label":_("Unit No"),
                "fieldname":"unit_no",
                "fieldtype":"Int",
                "insert_after":"unit_info", 
            },
            {
                "label":_("Unit Area"),
                "fieldname":"unit_area",
                "fieldtype":"Float",
                "insert_after":"unit_no", 
            },
            {
                "label":_("Unit Floor"),
                "fieldname":"unit_floor",
                "fieldtype":"Int",
                "insert_after":"unit_area", 
            },
            {
                "label":_("Reserved"),
                "fieldname":"reserved",
                "fieldtype":"Check",
                "insert_after":"unit_floor", 
                "read_only":"1", 
            },
            {
                "label":_("Unit details"),
                "fieldname":"unit_details",
                "fieldtype":"Small Text",
                "insert_after":"reserved", 
            },
        ],

        'Sales Order':[
            {
                "label": "Advance Payment",
                "fieldname": "advance_paymentss",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule"
            },
            {
                "label": "Get Advances Receivedd",
                "fieldname": "get_advancess",
                "fieldtype": "Button",
                "insert_after": "advance_paymentss",
                "allow_on_submit":1
            },
            {
                "label": "Advances",
                "fieldname": "advancess",
                "fieldtype": "Table",
                "options":"Sales Invoice Advance",
                "insert_after": "get_advancess",
                "allow_on_submit":1
            },
             
         ],
        
    },
      "properties": [

    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}







