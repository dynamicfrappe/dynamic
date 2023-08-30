

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Customer':[
             {
                "label":_("Branches"),
                "fieldname":"sec_branches",
                "fieldtype":"Section Break",
                "insert_after":"default_price_list", 
                "collapsible ":1 
            },
            {
                "label":_("Branches Table"),
                "fieldname":"branches",
                "fieldtype":"Table",
                "options":"Branches Table",
                "insert_after":"sec_branches", 
            },
            
        ],
        'Quotation':[
             {
                "label":_("Branches"),
                "fieldname":"sec_branches",
                "fieldtype":"Section Break",
                "insert_after":"ignore_pricing_rule", 
                "collapsible ":1 
            },
            {
                "label":_("Customer Branch"),
                "fieldname":"customer_branch",
                "fieldtype":"Link",
                "options":"Customer Branch",
                "insert_after":"sec_branches", 
            },
            
        ],
        'Sales Order':[
             {
                "label":_("Branches"),
                "fieldname":"sec_branches",
                "fieldtype":"Section Break",
                "insert_after":"ignore_pricing_rule", 
                "collapsible ":1 
            },
            {
                "label":_("Customer Branch"),
                "fieldname":"customer_branch",
                "fieldtype":"Link",
                "options":"Customer Branch",
                "insert_after":"sec_branches", 
            },
            
        ],
        'Sales Invoice':[
             {
                "label":_("Branches"),
                "fieldname":"sec_branches",
                "fieldtype":"Section Break",
                "insert_after":"ignore_pricing_rule", 
                "collapsible ":1 
            },
            {
                "label":_("Customer Branch"),
                "fieldname":"customer_branch",
                "fieldtype":"Link",
                "options":"Customer Branch",
                "insert_after":"sec_branches", 
            },
            
        ],
        'Delivery Note':[
             {
                "label":_("Branches"),
                "fieldname":"sec_branches",
                "fieldtype":"Section Break",
                "insert_after":"ignore_pricing_rule", 
                "collapsible ":1 
            },
            {
                "label":_("Customer Branch"),
                "fieldname":"customer_branch",
                "fieldtype":"Link",
                "options":"Customer Branch",
                "insert_after":"sec_branches", 
            },
            
        ],
        
    },
      "properties": [
        
    ],
  
    'on_setup': 'dynamic.branch.setup.create_branch_script'
}







