

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Stock Entry':[
            {
                "label":_("Real State Cost"),
                "fieldname":"real_state_cost",
                "fieldtype":"Link",
                "options":"Real State Cost",
                "read_only":"1", 
                "insert_after":"total_amount", 
            },
        ],
        'Landed Cost Taxes and Charges':[
            {
                "label":_("Cost Center"),
                "fieldname":"taxes_cost_center",
                "fieldtype":"Link",
                "insert_after":"base_amount", 
                "options":"Cost Center", 
                "in_list_view":"1", 
            },
        ],
        'Lead':[
            {
                "label":_("Call Type"),
                "fieldname":"call_type",
                "fieldtype":"Select",
                "insert_after":"contact_by", 
                "options":"\nFresh Call\nCold Call",
            },
        ],
        'Opportunity':[
            {
                "label":_("Note"),
                "fieldname":"note",
                "fieldtype":"Small Text",
                "insert_after":"source", 
            },
        ],
        'Item':[
            {
                "label":_("Unit Info"),
                "fieldname":"unit_info",
                "fieldtype":"Section Break",
                "insert_after":"image", 
            },
            {
                "label":_("Idoor Price"),
                "fieldname":"indoor_price",
                "fieldtype":"Currency",
                "insert_after":"standard_rate", 
            },
            {
                "label":_("Outdoor Price"),
                "fieldname":"outdoor_price",
                "fieldtype":"Currency",
                "insert_after":"indoor_price", 
            },
            {
                "label":_("Total Price"),
                "fieldname":"total_price",
                "fieldtype":"Currency",
                "insert_after":"outdoor_price", 
            },
            {
                "label":_("Unit No"),
                "fieldname":"unit_no",
                "fieldtype":"Int",
                "insert_after":"unit_info", 
            },
            {
                "label":_("Unit Area"),
                "fieldname":"unit_area",
                "fieldtype":"Float",
                "insert_after":"unit_no", 
            },
            {
                "label":_("Unit Floor"),
                "fieldname":"unit_floor",
                "fieldtype":"Int",
                "insert_after":"unit_area", 
            },
            {
                "label":_("Unit Floor Text"),
                "fieldname":"unit_floor_text",
                "fieldtype":"Data",
                "insert_after":"unit_floor", 
            },
            {
                "label":_("Reserved"),
                "fieldname":"reserved",
                "fieldtype":"Check",
                "insert_after":"unit_floor_text", 
                "read_only":"1", 
            },
            {
                "label":_("Unit details"),
                "fieldname":"unit_details",
                "fieldtype":"Small Text",
                "insert_after":"reserved", 
            },
            {
                "label":_("Unit Area Details"),
                "fieldname":"unit_area_section",
                "fieldtype":"Section Break",
                "insert_after":"unit_details", 
                "collapsible": 1,
            },
            {
                "label":_("Building Number"),
                "fieldname":"building_number",
                "fieldtype":"Int",
                "insert_after":"unit_area_section", 
            },
            {
                "label":_("Vaild To"),
                "fieldname":"vaild_to",
                "fieldtype":"Date",
                "insert_after":"building_number", 
            }, 
            {
                "label":_("Status"),
                "fieldname":"status",
                "fieldtype":"Select",
                "options" : "\nReserved\nAvailable To Sell",
                "insert_after":"vaild_to", 
                "read_only" : 1
            },    
            {
                "fieldname": "colum_break_install_vaild_to",
                "fieldtype": "Column Break",
                "insert_after": "stalus",
                "label": "",
            },
            {
                "label":_("Area Indoor"),
                "fieldname":"area_indoor",
                "fieldtype":"Float",
                "insert_after":"colum_break_install_vaild_to", 
            },
            {
                "label":_("Area Outdoor"),
                "fieldname":"area_outdoor",
                "fieldtype":"Float",
                "insert_after":"area_indoor", 
            },
        ],
        'Quotation':[
           {
                "label":_("Proker"),
                "fieldname":"section_break_table",
                "fieldtype":"Section Break",
                "insert_after":"terms", 
                "collapsible": 1,
            },
            {
                "label":_("Project"),
                "fieldname":"project",
                "fieldtype":"Data",
                "insert_after":"order_type", 
            },
            {
                "label":_("Proker"),
                "fieldname":"proker",
                "fieldtype":"Table",
                "options":"Sales Team", 
                "insert_after":"section_break_table", 
            },
            {
                "label":_("Sales Team"),
                "fieldname":"section_break_sales",
                "fieldtype":"Section Break",
                "insert_after":"proker", 
                "collapsible": 1,
            },
            {
                "label":_("Sales Team"),
                "fieldname":"sales_team_1",
                "fieldtype":"Table",
                "options":"Sales Team", 
                "insert_after":"section_break_sales", 
            },
            {
                "label":_("Maintenance Payment"),
                "fieldname":"maintenance_payment",
                "fieldtype":"Float",
                "insert_after":"total_taxes_and_charges", 
            },
            {
                "label":_("Warehouse Amount"),
                "fieldname":"warehouse_amount",
                "fieldtype":"Float",
                "insert_after":"maintenance_payment", 
            },
        ],
        'Sales Order':[
            {
                "label":_("Broker"),
                "fieldname":"section_break_table",
                "fieldtype":"Section Break",
                "insert_after":"total_commission", 
                "collapsible": 1,
            },
            {
                "label":_("Broker"),
                "fieldname":"broker",
                "fieldtype":"Table",
                "options":"Sales Team", 
                "insert_after":"section_break_table", 
            },
        ],
        'Quotation Item':[
            {
                "label":_("Area Indoor"),
                "fieldname":"area_indoor",
                "fieldtype":"Float",
                "insert_after":"item_code", 
                "fetch_from": "item_code.area_indoor",
            },
            {
                "label":_("Area Outdoor"),
                "fieldname":"area_outdoor",
                "fieldtype":"Float",
                "insert_after":"area_indoor", 
                "fetch_from": "item_code.area_outdoor",
            },
            {
                "label":_("Total Price"),
                "fieldname":"total_price",
                "fieldtype":"Float",
                "insert_after":"area_outdoor", 
                "fetch_from": "item_code.total_price",
            },
        ]
        # This commented because we trnasfer fields to Dynamic Account Domain
        # 'Sales Order':[
        #     {
        #         "label": "Advance Payment",
        #         "fieldname": "advance_paymentss",
        #         "fieldtype": "Section Break",
        #         "insert_after": "payment_schedule"
        #     },
        #     {
        #         "label": "Get Advances Receivedd",
        #         "fieldname": "get_advancess",
        #         "fieldtype": "Button",
        #         "insert_after": "advance_paymentss",
        #         "allow_on_submit":1
        #     },
        #     {
        #         "label": "Advances",
        #         "fieldname": "advancess",
        #         "fieldtype": "Table",
        #         "options":"Sales Invoice Advance",
        #         "insert_after": "get_advancess",
        #         "allow_on_submit":1
        #     },
        #     {
        #         "label": _("Outstanding Amount"),
        #         "fieldname": "outstanding_amount",
        #         "fieldtype": "Float",
        #         "insert_after": "advance_paid",
        #         "allow_on_submit":1,
        #         "read_only" : 1
        #     },
             
        #  ],
        
        
    },
      "properties": [
         {
            "doctype": "Payment Terms Template Detail",
            "doctype_or_field": "DocField",
            "fieldname": "due_date_based_on",
            "property": "default",
            "property_type": "Text",
            "value": "Month(s) after the end of the invoice month",
        },
        # {
        #     "doctype": "Quotation",
        #     "doctype_or_field": "DocField",
        #     "fieldname": "selling_price_list",
        #     "property": "reqd",
        #     "property_type": "Check",
        #     "value": "1",
        # },
        # {
        #     "doctype": "Quotation",
        #     "doctype_or_field": "DocField",
        #     "fieldname": "selling_price_list",
        #     "property": "hidden",
        #     "property_type": "Check",
        #     "value": "1",
        # },
        {
            "doctype": "Quotation",
            "doctype_or_field": "DocField",
            "fieldname": "ignore_pricing_rule",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },
        {
            "doctype": "Lead",
            "doctype_or_field": "DocField",
            "fieldname": "notes",
            "property": "reqd",
            "property_type": "Check",
            "value": "1",
        },
        {
            "doctype": "Sales Order",
            "doctype_or_field": "DocField",
            "fieldname": "sales_team_section_break",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },
        {
            "doctype": "Sales Order",
            "doctype_or_field": "DocField",
            "fieldname": "sales_partner",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },        
        {
            "doctype": "Sales Order",
            "doctype_or_field": "DocField",
            "fieldname": "amount_eligible_for_commission",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },        
        {
            "doctype": "Sales Order",
            "doctype_or_field": "DocField",
            "fieldname": "commission_rate",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },        
        {
            "doctype": "Sales Order",
            "doctype_or_field": "DocField",
            "fieldname": "total_commission",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },
    ],
    #
    # 'on_setup': 'dynamic.teba.setup.setup_teba'ignore_pricing_rule
}







