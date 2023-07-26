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
       ]
    }
}
