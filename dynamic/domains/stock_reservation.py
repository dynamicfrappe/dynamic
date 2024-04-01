
from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        "Stock Settings":
        [ 
            {
                "label": "Stock Reservation",
                "fieldname": "section_break_101",
                "fieldtype": "Section Break",
                "insert_after": "disable_serial_no_and_batch_selector" ,
            },
            {
                "label": "Enable Stock Reservation",
                "fieldname": "enable_stock_reservation",
                "fieldtype": "Check",
                "insert_after": "section_break_101" ,
                "description": "Allows to keep aside a specific quantity of inventory for a particular order."
            }, 
            {
                "label": "",
                "fieldname": "column_break_101",
                "fieldtype": "Column Break",
                "insert_after": "enable_stock_reservation" ,
            },
            {
                "label": "Allow Partial Reservation",
                "fieldname": "allow_partial_reservation",
                "fieldtype": "Check",
                "insert_after": "column_break_101" ,
                "description": "Partial stock can be reserved. For example, If you have a Sales Order of 100 units and the Available Stock is 90 units then a Stock Reservation Entry will be created for 90 units.",
                "depends_on": "eval: doc.enable_stock_reservation == 1"
            },
            {
                "label": "Auto Reserve Stock in Warehouse",
                "fieldname": "auto_reserve_stock_in_warehouse",
                "fieldtype": "Check",
                "insert_after": "allow_partial_reservation" ,
                # "description": "Stock will be reserved on submission of Purchase Receipt created against Material Receipt for Sales Order.",
                "depends_on": "eval: doc.enable_stock_reservation == 1"
            },
            {
                "label": "Warehouse",
                "fieldname": "warehouse",
                "fieldtype": "Link",
                "insert_after": "auto_reserve_stock_in_warehouse" ,
                "depends_on": "eval: doc.auto_reserve_stock_in_warehouse == 1",
                "options":"Warehouse"
            },
        ],
        "Sales Order":[
            {
                "label": "Reserve Stock",
                "fieldname": "reserve_stock",
                "fieldtype": "Check",
                "insert_after": "order_type" ,
                "depends_on": "eval: (doc.docstatus == 0 || doc.reserve_stock)",
                "description": "If checked, Stock will be reserved on <b>Submit</b>"
            },
            {
                "label": "Reserved for warehouse",
                "fieldname": "reserve_for_warehouse",
                "fieldtype": "Link",
                "insert_after": "set_warehouse" ,
                "read_only": 1 ,
                "options":"Warehouse"
            },
        ],
        "Stock Entry":[
            {
                "label": "Refrence Sales Order",
                "fieldname": "ref_sales_order",
                "fieldtype": "Link",
                "insert_after": "from_warehouse" ,
                "options":"Sales Order",
                "read_only": 1
            },
        ],
        "Stock Entry Detail":[
            {
                "label": "Refrence Sales Order",
                "fieldname": "ref_sales_order",
                "fieldtype": "Link",
                "insert_after": "job_card_item" ,
                "options":"Sales Order",
                "read_only": 1
            },
            {
                "label": "Refrence Index",
                "fieldname": "ref_idx",
                "fieldtype": "Data",
                "insert_after": "ref_sales_order" ,
                "read_only": 1
            },
        ]
    },
     "properties": [
        {
        # "doctype": "Sales Invoice",
        # "doctype_or_field": "DocField",
        # "fieldname": "customer_name",
        # "property": "read_only",
        # "property_type": "Check",
        # "value": "0"
        },
     ]
}