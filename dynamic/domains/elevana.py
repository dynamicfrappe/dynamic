from __future__ import unicode_literals

data = {

    'custom_fields': {
        'Lead': [
            {
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "campaign_name",
                "label": "Sales Person",
                "options": "Sales Person",
                "permlevel": "1"
            }
        ],

        'Opportunity': [
            {
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "source",
                "label": "Sales Person",
                "options": "Sales Person",
                # "permlevel":"1"
            }
        ],
        'Customer': [
            {
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "insert_after": "opportunity_name",
                "label": "Sales Person",
                "options": "Sales Person",
                # "permlevel":"1"
            },
            {
                "fieldname": "ref_doctype",
                "fieldtype": "Link",
                "insert_after": "sales_person",
                "label": "Reference Type",
                "options": "DocType",
                "read_only": "1",
            },
            {
                "fieldname": "ref_docname",
                "fieldtype": "Dynamic Link",
                "insert_after": "ref_doctype",
                "label": "Reference Name",
                "options": "ref_doctype",
                "read_only": "1",
            }
        ],
        
        'Sales Partner': [
            {
                "fieldname": "ref_doctype",
                "fieldtype": "Link",
                "insert_after": "commission_rate",
                "label": "Reference Type",
                "options": "DocType",
                "read_only": "1",
            },
            {
                "fieldname": "ref_docname",
                "fieldtype": "Dynamic Link",
                "insert_after": "ref_doctype",
                "label": "Reference Name",
                "options": "ref_doctype",
                "read_only": "1",
            },
            {
                "fieldname": "item_groups_section_break",
                "fieldtype": "Section Break",
                "insert_after": "targets",
                "label": "Item Groups",
            },
            {
                "fieldname": "item_groups",
                "fieldtype": "Table",
                "insert_after": "item_groups_section_break",
                "label": "Item Groups",
                "options": "Item Group Detail",
            },
        ],
        'Coupon Code': [
            {
                "fieldname": "ref_doctype",
                "fieldtype": "Link",
                "insert_after": "amended_from",
                "label": "Reference Type",
                "options": "DocType",
                "read_only": "1",
            },
            {
                "fieldname": "ref_docname",
                "fieldtype": "Dynamic Link",
                "insert_after": "ref_doctype",
                "label": "Reference Name",
                "options": "ref_doctype",
                "read_only": "1",
            }
        ],
        
        'Quotation': [
            {
                "fieldname": "sales_team_section_break",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule",
                "label": "Sales Team",
            },
            {
                "fieldname": "sales_team",
                "fieldtype": "Table",
                "insert_after": "sales_team_section_break",
                "label": "Sales Team",
                "options": "Sales Team"
            }
        ],
        'Selling Settings': [

            {
                "fieldname": "defatults_distributor_marketer_section_break",
                "fieldtype": "Section Break",
                "insert_after": "hide_tax_id",
                "label": "Distributor & Marketer",
            },
            {
                "fieldname": "default_distributor_territory",
                "fieldtype": "Link",
                "insert_after": "defatults_distributor_marketer_section_break",
                "label": "Default Distributor Territory",
                "options": "Territory"
            },
            {
                "fieldname": "default_distributer_customer_group",
                "fieldtype": "Link",
                "insert_after": "default_distributor_territory",
                "label": "Default Distributor Customer Group",
                "options": "Customer Group"
            },
            {
                "fieldname": "defatults_distributor_marketer_column_break",
                "fieldtype": "Column Break",
                "insert_after": "default_distributor_territory",
                "label": "",
            },
            {
                "fieldname": "default_marketer_territory",
                "fieldtype": "Link",
                "insert_after": "defatults_distributor_marketer_column_break",
                "label": "Default Marketer Territory",
                "options": "Territory"
            },
            {
                "fieldname": "default_marketer_customer_group",
                "fieldtype": "Link",
                "insert_after": "default_marketer_territory",
                "label": "Default Marketer Customer Group",
                "options": "Customer Group"
            }
        ]

    },
    "properties": [
        {
            "doctype":"Customer",
            "doctype_or_field":"DocField",
            "fieldname":"customer_type",
            "property":"options",
            "property_type":"Text",
            "value": "\nCompany\nIndividual\nMarketer\nDistributor"
        }
    ],
    "property_setters": [

    ],
    'on_setup': 'dynamic.elevana.setup.install_elevana'
}
