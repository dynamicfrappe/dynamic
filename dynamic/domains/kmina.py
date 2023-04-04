

from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Sales Order':[
             {
                "label": "Manufacturer Name",
                "fieldname": "manufacturer_name",
                "fieldtype": "Data",
                "insert_after": "order_type",
            },
            {
                "label": "Shipment Type",
                "fieldname": "shipment_type",
                "fieldtype": "Select",
                "options":"\nAir Type\nSea Type",
                "insert_after": "manufacturer_name",
            },
        ],
        'Sales Invoice':[
             {
                "label": "Manufacturer Name",
                "fieldname": "manufacturer_name",
                "fieldtype": "Data",
                "insert_after": "customer",
            },
            {
                "label": "Shipment Type",
                "fieldname": "shipment_type",
                "fieldtype": "Select",
                "options":"\nAir Type\nSea Type",
                "insert_after": "manufacturer_name",
            },

        ],
    },
      "properties": [
    ],
  
    # 'on_setup': 'dynamic.kmina.setup.setup_kmina'
}







