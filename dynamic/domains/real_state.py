

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
                "fieldtype":"Data",
                "insert_after":"unit_area", 
            },
            {
                "label":_("Reserved"),
                "fieldname":"reserved",
                "fieldtype":"Check",
                "insert_after":"unit_floor", 
                "read_only":"1", 
            },
            {
                "label":_("Unit details"),
                "fieldname":"unit_details",
                "fieldtype":"Small Text",
                "insert_after":"reserved", 
            },
        ],
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
        #  'Quotation':[
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
        #         "insert_after": "in_words",
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
    ],
    #
    # 'on_setup': 'dynamic.teba.setup.setup_teba'ignore_pricing_rule
}







