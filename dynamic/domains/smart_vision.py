from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Sales Order':[

            {
                "label":"End User",
                "fieldname":"end_user",
                "fieldtype":"Link",
                "options":'Customer',
                "insert_after":"customer",
            },
            {
                "label":"End User",
                "fieldname":"end_user",
                "fieldtype":"Link",
                "options":'Customer',
                "insert_after":"customer",
            },
        ],
        'Customer':[
            {
                "label":"Email",
                "fieldname":"email",
                "fieldtype":"Data",
                "insert_after":"customer_name",
            },
        ],
        
    },
}