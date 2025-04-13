import frappe
from frappe import _



from __future__ import unicode_literals


data = {

    'custom_fields': {
        'Expense Claim':[
            {
                "label":_("Payment Methods"),
                "fieldname":"payment_methods",
                "fieldtype":"Data",
                "insert_after":"approval_status",
            },  
            {
                "label":_("Beneficiary Name"),
                "fieldname":"beneficiary_name",
                "fieldtype":"Data",
                "insert_after":"payment_methods"
            },
            {
                "label":_("Choose Currencies"),
                "fieldname":"choose_currencies",
                "fieldtype":"Data",
                "insert_after":"beneficiary_name", 
            },
        ],    
    },
      "properties": [
        # Sales Invoice Item
        
    ],
  
    # 'on_setup': 'dynamic.owais.setup.setup_owais'
}