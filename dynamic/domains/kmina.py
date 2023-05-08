

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
         'Sales Order Item':[
             {
                "label": "Batch KM",
                "fieldname": "batch_km",
                "fieldtype": "Data",
                "insert_after": "amount",
                "in_list_view": "1",
                "columns":1
            },
              {
                "label": "Manufacturing Date",
                "fieldname": "manfacturing_date",
                "fieldtype": "Date",
                "insert_after": "batch_km",
                "in_list_view": "1",
                "columns":1
            },
             {
                "label": "Expirtion Date",
                "fieldname": "expiration_date",
                "fieldtype": "Date",
                "insert_after": "manfacturing_date",
                "in_list_view": "1",
                "columns":1

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
                "label": "CIF",
                "fieldname": "cif",
                "fieldtype": "Small Text",
                "insert_after": "shipment_type",
            },


        ],
        'Sales Invoice Item':[
             {
                "label": "Batch KM",
                "fieldname": "batch_km",
                "fieldtype": "Data",
                "insert_after": "amount",
                "in_list_view": "1",
                "columns":1
            },
              {
                "label": "Manufacturing Date",
                "fieldname": "manfacturing_date",
                "fieldtype": "Date",
                "insert_after": "batch_km",
                "in_list_view": "1",
                "columns":1
            },
             {
                "label": "Expirtion Date",
                "fieldname": "expiration_date",
                "fieldtype": "Date",
                "insert_after": "manfacturing_date",
                "in_list_view": "1",
                "columns":1

            },
        ],
        #? purchase invoice
         'Purchase Invoice':[
            {
                "label": "FOB",
                "fieldname": "fob",
                "fieldtype": "Small Text",
                "insert_after": "due_date",
            },

        ],
        #? purchase invoice Item
         'Purchase Invoice Item':[
             {
                "label": "Batch KM",
                "fieldname": "batch_km",
                "fieldtype": "Data",
                "insert_after": "amount",
                "in_list_view": "1",
                "columns":1
            },
              {
                "label": "Manufacturing Date",
                "fieldname": "manfacturing_date",
                "fieldtype": "Date",
                "insert_after": "batch_km",
                "in_list_view": "1",
                "columns":1
            },
             {
                "label": "Expirtion Date",
                "fieldname": "expiration_date",
                "fieldtype": "Date",
                "insert_after": "manfacturing_date",
                "in_list_view": "1",
                "columns":1

            },
        ],
        #? purchase Order Item
         'Purchase Order Item':[
             {
                "label": "Batch KM",
                "fieldname": "batch_km",
                "fieldtype": "Data",
                "insert_after": "amount",
                "in_list_view": "1",
                "columns":1
            },
            {
                "label": "Manufacturing Date",
                "fieldname": "manfacturing_date",
                "fieldtype": "Date",
                "insert_after": "batch_km",
                "in_list_view": "1",
                "columns":1
            },
             {
                "label": "Expirtion Date",
                "fieldname": "expiration_date",
                "fieldtype": "Date",
                "insert_after": "manfacturing_date",
                "in_list_view": "1",
                "columns":1

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

        #? Sales Invoice Item 
        {
            "doctype": "Sales Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "item_code",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Sales Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "qty",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Sales Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "rate",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Sales Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "description",
            "property": "in_list_view",
            "property_type": "Check",
            "value": "0"
        },
        #? purchase invoice Item 
        {
            "doctype": "Purchase Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "item_code",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Purchase Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "qty",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Purchase Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "rate",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Purchase Invoice Item",
            "doctype_or_field": "DocField",
            "fieldname": "amount",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        #? Purchase Order Item 
        {
            "doctype": "Purchase Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "item_code",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Purchase Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "schedule_date",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Purchase Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "qty",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Purchase Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "uom",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Purchase Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "rate",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Purchase Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "amount",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        #? Sales Order Item 
        {
            "doctype": "Sales Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "item_name",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Sales Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "item_code",
            "property": "columns",
            "property_type": "Int",
            "value": "2"
        },
        {
            "doctype": "Sales Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "delivery_date",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Sales Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "qty",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Sales Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "rate",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
        {
            "doctype": "Sales Order Item",
            "doctype_or_field": "DocField",
            "fieldname": "amount",
            "property": "columns",
            "property_type": "Int",
            "value": "1"
        },
       
      
    ],
  
    # 'on_setup': 'dynamic.kmina.setup.setup_kmina'
}







