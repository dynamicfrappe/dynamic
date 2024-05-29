from __future__ import unicode_literals
from frappe import _

data = {

    'custom_fields': {
        "Item":[
               {
                    "fieldname":"item_parent_group",
                    "fieldtype":"Link",
                    "insert_after":"item_group",
                    "label":"Parent Group",
                    "read_only" : 1 ,
                    "options" :'Item Group',
              
               },

               ],
     "Material Request":[
        {
            "fieldname":"material_request_purpose",
            "fieldtype":"Link",
            "insert_after":"material_request_type",
            "label":"Material Request Purpose",
            "options" :'Material Request Purpose',
            "reqd":1
        },
     ],
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
       "Warehouse" :[
            {
            "label":_("User Allowed"),
            "fieldname":"user_allowed",
            "fieldtype":"Section Break",
            "insert_after":"old_parent",
            },
            {
            "label":_("Users"),
            "fieldname":"users",
            "fieldtype":"Table",
            "insert_after":"user_allowed",
            "options":"Warehouse User",
            },
           
       ],

     #   "User" :[
     #      {"lable" :"Defaulte Warehouse"  ,
     #        "fieldname":"defaulte_ware_house",
     #        "fieldtype":"Link",
     #        "insert_after":"user_allowed",
     #        "options":"Warehouse User",
          
     #      }
     #  ]
    },"properties": [
     {
        "doctype": "Material Request",
        "doctype_or_field": "DocField",
        "fieldname": "material_request_type",
        "property": "reqd",
        "property_type": "Check",
        "value": "0"
        },
        {
        "doctype": "Material Request",
        "doctype_or_field": "DocField",
        "fieldname": "material_request_type",
        "property": "read_only",
        "property_type": "Check",
        "value": "1"
        },
    ]
}
