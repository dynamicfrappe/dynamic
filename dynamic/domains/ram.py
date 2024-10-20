from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    
    'custom_fields': {
        "Target Detail":
        [
            {
                "label": "Item Code",
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "insert_after": "" ,
                "reqd": 1,
                "in_list_view": 1,
            },
        ],
    },
    "properties": [
        {
            "doctype": "Pricing Rule",
            "doctype_or_field": "DocField",
            "fieldname": "customer",
            "property": "options",
            "property_type": "Text",
            "value": "Customer Table"
        },
        {
            "doctype": "Pricing Rule",
            "doctype_or_field": "DocField",
            "fieldname": "customer",
            "property": "fieldtype",
            "property_type": "Select",
            "value": "Table"
        },


        # {
        # "name": "item_group_fetch_from",
        # "doc_type": "Target Detail",
        # "doctype_or_field": "DocField",
        # "field_name" : "item_group",
        # "property": "fetch_from",
        # "property_type": "Data",
        # "value": "item_code.item_group"
        # },

        # {
        # "name": "item_group_in_list_view",
        # "doc_type": "Target Detail",
        # "doctype_or_field": "DocField",
        # "field_name" : "item_group",
        # "property": "in_list_view",
        # "property_type": "Check",
        # "value": "0"
        # }, 
    ],
    'on_setup' : 'dynamic.ram.controllers.setup.create_property_setter'

}