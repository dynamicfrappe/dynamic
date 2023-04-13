

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
             {
                "label": "Batch No",
                "fieldname": "batch_no",
                "fieldtype": "Data",
                "insert_after": "shipment_type",
            },
             {
                "label": "Manufacturing Date",
                "fieldname": "manfacturing_date",
                "fieldtype": "Date",
                "insert_after": "batch_no",
            },
             {
                "label": "Expirtion Date",
                "fieldname": "expiration_date",
                "fieldtype": "Date",
                "insert_after": "manfacturing_date",
            },
             {
                "label": "CIF",
                "fieldname": "cif",
                "fieldtype": "Small Text",
                "insert_after": "expiration_date",
            },


        ],
         'Purchase Invoice':[
             {
                "label": "Batch No",
                "fieldname": "batch_no",
                "fieldtype": "Data",
                "insert_after": "due_date",
            },
             {
                "label": "Manufacturing Date",
                "fieldname": "manfacturing_date",
                "fieldtype": "Date",
                "insert_after": "batch_no",
            },
             {
                "label": "Expirtion Date",
                "fieldname": "expiration_date",
                "fieldtype": "Date",
                "insert_after": "manfacturing_date",
            },
            {
                "label": "FOB",
                "fieldname": "fob",
                "fieldtype": "Small Text",
                "insert_after": "expiration_date",
            },

        ],
         'Customer':[
             {
                "label": "HS Code",
                "fieldname": "hs_code",
                "fieldtype": "Data",
                "insert_after": "tax_id",
            },
            {
                "label": "SDFA Code",
                "fieldname": "sdfa_code",
                "fieldtype": "Data",
                "insert_after": "hs_code",
            },
         ]
    },
      "properties": [
    ],
  
    # 'on_setup': 'dynamic.kmina.setup.setup_kmina'
}







