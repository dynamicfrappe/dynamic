

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {


        'Item':[
            {
                "label":_("Next Item Name"),
                "fieldname":"next_name",
                "fieldtype":"Data",
                "insert_after":"naming_series", 
                "read_only":1, 
            },
            {
                "label":_("Last Item"),
                "fieldname":"last_item",
                "fieldtype":"Data",
                "insert_after":"account_currency",
                "read_only":1, 
            },
            
        ],
        'Supplier':[
            {
                "label":_("Supplier Code"),
                "fieldname":"supplier_code",
                "fieldtype":"Data",
                "insert_after":"supplier_name", 
                "in_global_search":1, 
            },
            {
                "label":_("Last Supplier"),
                "fieldname":"last_supplier",
                "fieldtype":"Data",
                "insert_after":"naming_series", 
                "read_only":1, 

            },
            
        ],
        'Stock Entry Detail':[
                {
                "label":_("Available Qty"),
                "fieldname":"available_qty",
                "fieldtype":"Float",
                "insert_after":"actual_qty", 
                "read_only":1
              
            },
        ],
        'Delivery Note Item':[
               {
                "label":_("Available Qty"),
                "fieldname":"available_qty",
                "fieldtype":"Float",
                "insert_after":"stock_qty", 
                "read_only":1
              
            },
        ],
        'Purchase Receipt Item':[
            {
                "label":_("Available Qty"),
                "fieldname":"available_qty",
                "fieldtype":"Float",
                "insert_after":"stock_qty", 
                "read_only":1
            }
        ],
        'Customer':[
            {
                "label":_("Customer Code"),
                "fieldname":"customer_code",
                "fieldtype":"Data",
                "insert_after":"customer_name", 
                "in_global_search":1, 
            },
            {
                "label":_("Last Customer"),
                "fieldname":"last_customer",
                "fieldtype":"Data",
                "insert_after":"salutation", 
                "read_only":1, 
            },
            
        ],
        'Warehouse':[
            {
                "label":_("Warehouse Code"),
                "fieldname":"warehouse_code",
                "fieldtype":"Data",
                "insert_after":"parent_warehouse", 
                "in_global_search":1, 
            },
            
        ],
        
        'Journal Entry':[
            {
                "label":_("Notebook No"),
                "fieldname":"notebook_no",
                "fieldtype":"Data",
                "insert_after":"multi_currency", 
            },
            {
                "label":_("Main Currency"),
                "fieldname":"main_currency",
                "fieldtype":"Check",
                "insert_after":"voucher_type", 
            },
            {
                "label":_("Account Currency"),
                "fieldname":"account_currency",
                "fieldtype":"Link",
                "insert_after":"main_currency",  
                "options":"Currency", 

            },
            
        ],
        'Selling Settings':[
            {
                "label":_("Sales Serries"),
                "fieldname":"sales_series_section",
                "fieldtype":"Section Break",
                "insert_after":"allow_sales_order_creation_for_expired_quotation", 
            },
            {
                "label":_("Series Role"),
                "fieldname":"series_role",
                "fieldtype":"Table",
                "options":"Sales Naming Series Role",
                "insert_after":"sales_series_section", 
            },
            {
                "label":_("Check Actual QTY IN Save"),
                "fieldname":"check_qty",
                "fieldtype":"Check",
                "insert_after":"series_role", 
            },
            
        ],
        
        
    },
      "properties": [
        {
        "doctype": "Item Barcode",
        "doctype_or_field": "DocField",
        "fieldname": "barcode",
        "property": "read_only",
        "property_type": "Check",
        "value": "0"
        },
        {
        "doctype": "Purchase Receipt Item",
        "doctype_or_field": "DocField",
        "fieldname": "stock_uom_rate",
        "property": "read_only",
        "property_type": "Check",
        "value": "0"
        },
        
        {
        "doctype": "Delivery Note Item",
        "doctype_or_field": "DocField",
        "fieldname": "stock_uom_rate",
        "property": "read_only",
        "property_type": "Check",
        "value": "0"
        },
    ],
  
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}







