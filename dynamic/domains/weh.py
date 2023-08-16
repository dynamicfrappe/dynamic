from __future__ import unicode_literals


data = {

    'custom_fields': {
       "Customer":[
        {
            "fieldname":"remote_id",
            "fieldtype":"Data",
            "insert_after":"naming_series",
            "label":"remote_id",
            "read_only" :1
        },
         {
            "fieldname":"doctor",
            "fieldtype":"Data",
            "insert_after":"territory",
            "label":"Doctor",
            "read_only" :1
            },
            {
            "fieldname":"branch",
            "fieldtype":"Data",
            "insert_after":"doctor",
            "label":"Branch",
            "read_only" :1
            } ,
              {
            "fieldname":"surgery",
            "fieldtype":"Data",
            "insert_after":"branch",
            "label":"Surgery",
            "read_only" :1
            }
       ] ,
       "Delivery Note" :[
            {
            "fieldname":"doctor",
            "fieldtype":"Data",
            "insert_after":"title",
            "label":"Doctor",
            "read_only" :1
            },
            {
            "fieldname":"branch",
            "fieldtype":"Data",
            "insert_after":"doctor",
            "label":"Branch",
            "read_only" :1
            } ,
              {
            "fieldname":"surgery",
            "fieldtype":"Data",
            "insert_after":"branch",
            "label":"Surgery",
            "read_only" :1
            }
       ] ,
       "Purchase Invoice" :[
            {
            "fieldname":"real_date",
            "fieldtype":"Date",
            "insert_after":"due_date",
            "label":"Invoice Date",
            "read_only" :0
            },
           
       ],
       "Stock Entry Detail" :[
            {
            "label":"Actual Qty(Target)",
            "fieldname":"qty_target",
            "fieldtype":"Float",
            "insert_after":"actual_qty",
            "read_only" :1
            },
           
       ],
    }
}
