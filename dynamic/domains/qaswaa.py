
from __future__ import unicode_literals
import frappe
from frappe import _

data = {


    'custom_fields': {
        "Sales Order":
        [ 
            {
                "label": "Notes",
                "fieldname": "notes",
                "fieldtype": "Small Text",
                "insert_after": "to_date" ,
            },
            {
                "label": "Item Discount rate",
                "fieldname": "item_discount_rate",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
            },
        ],
        "Quotation":
        [ 
           
            {
                "label": "Sales Team",
                "fieldname": "sales_team_section_break_",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule" ,
            },
            {
                "label": "Sales Team Qt",
                "fieldname": "sales_team_qt",
                "fieldtype": "Table",
                "insert_after": "sales_team_section_break_" ,
                "options":"Sales Team",
            },
            {
                "label": "Notes",
                "fieldname": "notes",
                "fieldtype": "Small Text",
                "insert_after": "source" ,
            },
            {
                "label": "Account Dimension",
                "fieldname": "account_dimension_section",
                "fieldtype": "Section Break",
                "insert_after": "order_type" ,
            },
            {
                "label": "Cost Center",
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "insert_after": "account_dimension_section" ,
                "options":"Cost Center",
            },
            {
                "label": "",
                "fieldname": "column_break_1100",
                "fieldtype": "Column Break",
                "insert_after": "cost_center" ,
            },
            {
                "label": "Warehouse",
                "fieldname": "warehouse",
                "fieldtype": "Link",
                "insert_after": "column_break_1100" ,
                "options":"Warehouse",
            },
            {

                "label": "Item Discount rate",
                "fieldname": "item_discount_rate",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
            } 
        
        ],
        "Quotation Item":
        [ 
           
            {
                "label": "Item Name Print",
                "fieldname": "item_name_print",
                "fieldtype": "Data",
                "insert_after": "item_name" ,
            },
        ],
        "Item Group":
        [ 
           
            {
                "label": "Group Code",
                "fieldname": "group_code",
                "fieldtype": "Data",
                "insert_after": "column_break_5" ,
            },
        
        ],
        "Sales Invoice":
        [ 
            {
                "label": "Customer Name.",
                "fieldname": "customer_name_hand",
                "fieldtype": "Data",
                "insert_after": "customer_name" ,
            },
            {
                "label": "Notes",
                "fieldname": "notes",
                "fieldtype": "Small Text",
                "insert_after": "to_date" ,
            },
            {

                "label": "Item Discount rate",
                "fieldname": "item_discount_rate",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
            }
          
        ],
        "Selling Settings":
        [
            {
                "label": "Apply Reservation",
                "fieldname": "apply_reservation",
                "fieldtype": "Check",
                "insert_after": "territory" ,
            },
        ],
        "Stock Entry Type":
        [
            {
                "label": "Mendatory Fields",
                "fieldname": "mendatory_fields",
                "fieldtype": "Check",
                "insert_after": "purpose" ,
            },

            {
                "label": "Matrial Type",
                "fieldname": "matrial_type",
                "fieldtype": "Select",
                "insert_after": "mendatory_fields" ,
                "options":"\nDispensing Simples\nReceived Simples\nDispensing Gift"
            },

        ],
        "Stock Entry":
        [
             {
                "label": "Mendatory Fields",
                "fieldname": "mendatory_fields",
                "fieldtype": "Check",
                "insert_after": "sales_team" ,
                "fetch_from":"stock_entry_type.mendatory_fields",
                # "hidden": 1
            },
            {
                "label": "Customer",
                "fieldname": "customer_id",
                "fieldtype": "Link",
                "insert_after": "stock_entry_type",
                "options": "Customer",
                "depends_on":"eval:doc.mendatory_fields == true",
                "mandatory_depends_on":"eval:doc.mendatory_fields == true"
            },

			{
				"label": "Old Stock Entry",
				"fieldname": "old_stock_entry",
				"fieldtype": "Link",
				"insert_after": "customer_id",
				"options": "Stock Entry",
				"hidden": 1,
			},

            {
                "label": "Sales Team",
                "fieldname": "sales_team",
                "fieldtype": "Table",
                "insert_after": "get_stock_and_rate",
                "options": "Sales Team",
                "depends_on": "eval:doc.mendatory_fields == true",
            },
        ],
        "Item":[
            {
				"label": "Material",
				"fieldname": "material",
				"fieldtype": "Link",
				"insert_after": "brand" ,
				"options":"Material",
			},
			{
				"label": "Origin",
				"fieldname": "origin",
				"fieldtype": "Link",
				"insert_after": "material" ,
				"options":"Origin",
			},
			{
				"label": "Electroic Code",
				"fieldname": "electroic_code",
				"fieldtype": "Link",
				"insert_after": "origin" ,
				"options":"Electroic Code",
			},
 
			{
				"label": "Size",
				"fieldname": "size_",
				"fieldtype": "Link",
				"insert_after": "electroic_code" ,
				"options":"Size",
			},
			{
				"label": "Group Code",
				"fieldname": "group_code",
				"fieldtype": "Data",
				"insert_after": "size_" ,
			},
			{
				"label": "Group Code 2",
				"fieldname": "group_code2",
				"fieldtype": "Data",
				"insert_after": "group_code" ,
				"fetch_from": "item_group.group_code"
			},
			{
				"label": "Objective",
				"fieldname": "objective_",
				"fieldtype": "Link",
				"insert_after": "group_code2" ,
				"options":"Objective",
			},
            
        ],
        "Purchase Order":[
            {

                "label": "Item Discount rate",
                "fieldname": "item_discount_rate",
                "fieldtype": "Float",
                "insert_after": "discount_amount" ,
            } 
        ],
        "Cost Center":[
            {
				"label": "is Default",
				"fieldname": "is_default",
				"fieldtype": "Check",
				"insert_after": "enable_distributed_cost_center" ,
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
        {
            "doctype": "Sales Invoice",
            "doctype_or_field": "DocField",
            "fieldname": "sales_team",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "0",
        },
        {
            "doctype": "Sales Team",
            "doctype_or_field": "DocField",
            "fieldname": "sales_person",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "0",
        }, 
        {
            "doctype": "Sales Team",
            "doctype_or_field": "DocField",
            "fieldname": "allocated_percentage",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "0",
        }, 
        {
            "doctype": "Sales Team",
            "doctype_or_field": "DocField",
            "fieldname": "incentives",
            "property": "allow_on_submit",
            "property_type": "Check",
            "value": "0",
        },
        {
            "doctype": "Sales Invoice",
            "doctype_or_field": "DocField",
            "fieldname": "update_stock",
            "property": "read_only",
            "property_type": "Check",
            "value": "1",
        },
        {
            "doctype": "Sales Invoice",
            "doctype_or_field": "DocField",
            "fieldname": "update_stock",
            "property": "default",
            "value": "1",
        },

        {
            "doctype": "Purchase Invoice",
            "doctype_or_field": "DocField",
            "fieldname": "update_stock",
            "property": "read_only",
            "property_type": "Check",
            "value": "1",
        },
        {
            "doctype": "Purchase Invoice",
            "doctype_or_field": "DocField",
            "fieldname": "update_stock",
            "property": "default",
            "value": "1",
        },

        {
            "doctype": "Purchase Invoice",
            "doctype_or_field": "DocField",
            "fieldname": "cost_center",
            "property": "reqd",
            "property_type": "default",
            "value": "1",
        },
     ]

}