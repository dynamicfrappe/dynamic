from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Delivery Note': [
            {
                "label": "Voucher Number",
                "fieldname": "voucher_number",
                "fieldtype": "Data",
                "insert_after": "customer",
            }
        ],
        'Stock Reconciliation': [
            {
                "label": "Voucher Number",
                "fieldname": "voucher_number",
                "fieldtype": "Data",
                "insert_after": "purpose",
            }
        ],

       
    },
    "properties": [
       
    ],
    "property_setters": [

    ],
    # 'on_setup': 'dynamic.majestey.setup.install_majestey'
}
