from __future__ import unicode_literals

data = {
    'custom_fields': {
        'UOM': [
            {
                "fieldname": "english_description",
                "fieldtype": "Text",
                "insert_after": "must_be_whole_number",
                "label": "English Description",
                "name": "UOM-english_description",
            },
            {
                "fieldname": "arabic_description",
                "fieldtype": "Text",
                "insert_after": "english_description",
                "label": "Arabic Description",
                "name": "UOM-arabic_description",
            }
        ],
        'Customer': [
            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "represents_company",
                "label": "E Invoice Address",
                "name": "Customer-e_invoice_section_break",
            },
            {
                "fieldname": "receiver_type",
                "fieldtype": "Select",
                "insert_after": "e_invoice_section_break",
                "options": "P\nB\nF",
                "default": "P",
                "label": "Receiver Type",
                "name": "Customer-receiver_type",

                # "reqd": 1
            },
            {
                "fieldname": "receiver_id",
                "fieldtype": "Data",
                "insert_after": "receiver_type",
                "label": "Receiver ID",
                "name": "Customer-receiver_id",
                "mandatory_depends_on": "eval:doc.receiver_type=='P'"
                # "reqd":1
            },
            {
                "fieldname": "country_code",
                "fieldtype": "Link",
                "insert_after": "receiver_id",
                "label": "Country Code",
                "options": "Country Code",
                "name": "Customer-country_code",
                # "reqd": 1
            },
            {
                "fieldname": "governate",
                "fieldtype": "Data",
                "insert_after": "country_code",
                "label": "Governate",
                "name": "Customer-governate",
                # "reqd": 1
            },
            {
                "fieldname": "e_invoice_column_break",
                "fieldtype": "Column Break",
                "insert_after": "governate",
                "label": "",
                "name": "Customer-e_invoice_column_break",
                # "reqd":1
            },
            {
                "fieldname": "regioncity",
                "fieldtype": "Data",
                "insert_after": "e_invoice_column_break",
                "label": "Region City",
                "name": "Customer-regioncity",
                # "reqd": 1
            },
            {
                "fieldname": "street",
                "fieldtype": "Data",
                "insert_after": "regioncity",
                "label": "Street",
                "name": "Customer-street",
                # "reqd": 1
            },
            {
                "fieldname": "buildingnumber",
                "fieldtype": "Data",
                "insert_after": "street",
                "label": "Building Number",
                "name": "Customer-buildingnumber",
                # "reqd": 1
            },
            {
                "fieldname": "branchid",
                "fieldtype": "Data",
                "insert_after": "buildingnumber",
                "label": "Branch ID",
                "name": "Branch ID",
                # "reqd": 1
            },

        ],
        'Company': [
            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "parent_company",
                "label": "E Invoice Address",
            },
            {
                "fieldname": "issuer_type",
                "fieldtype": "Select",
                "insert_after": "e_invoice_section_break",
                "options": "P\nB\nF",
                "default": "P",
                "label": "Issuer Type",
                "reqd": 0
            },
            {
                "fieldname": "issuer_id",
                "fieldtype": "Data",
                "insert_after": "issuer_type",
                "label": "Issuer ID",
                "mandatory_depends_on": "eval:doc.issuer_type=='P'"
                # "reqd":1
            },
            {
                "fieldname": "activity_code",
                "fieldtype": "Data",
                "insert_after": "issuer_id",
                "label": "Activity Code",
                "reqd": 0,
            },
            {
                "fieldname": "country_code",
                "fieldtype": "Link",
                "insert_after": "activity_code",
                "label": "Country Code",
                "options": "Country Code",
                "name": "Company-country_code",
                "reqd": 0
            },
            {
                "fieldname": "governate",
                "fieldtype": "Data",
                "insert_after": "country_code",
                "label": "Governate",
                "name": "Company-governate",
                "reqd": 0
            },
            {
                "fieldname": "e_invoice_column_break",
                "fieldtype": "Column Break",
                "insert_after": "governate",
                "label": "",
                "name": "Company-e_invoice_column_break",
                # "reqd":1
            },
            {
                "fieldname": "regioncity",
                "fieldtype": "Data",
                "insert_after": "e_invoice_column_break",
                "label": "Region City",
                "name": "Company-regioncity",
                "reqd": 0
            },
            {
                "fieldname": "street",
                "fieldtype": "Data",
                "insert_after": "regioncity",
                "label": "Street",
                "name": "Company-street",
                "reqd": 0
            },
            {
                "fieldname": "buildingnumber",
                "fieldtype": "Data",
                "insert_after": "street",
                "label": "Building Number",
                "name": "Company-buildingnumber",
                "reqd": 0
            },

        ],
        'Item': [
            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "description",
                "label": ""
            },
            {
                "fieldname": "item_type",
                "fieldtype": "Select",
                "insert_after": "e_invoice_section_break",
                "label": "Item Type",
                "options": "GS1\nEGS",
                "in_filter": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "itemcode",
                "fieldtype": "Data",
                "insert_after": "item_type",
                "label": "Item Code",
                "in_filter": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "e_invoice_setting",
                "fieldtype": "Table",
                "insert_after": "itemcode",
                "label": "E Invoice Configuration",
                "options": "E Invoice Item Configuration",
                "in_filter": 1,
                "in_standard_filter": 1
            },
        ],
        'Sales Invoice': [
            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "cost_center",
                "label": "",
            },
            {
                "fieldname": "tax_auth",
                "fieldtype": "Check",
                "insert_after": "e_invoice_section_break",
                "label": "Tax Auth",
                "in_filter": 1,
                "in_standard_filter": 1
            },
            {
                "fieldname": "activity_code",
                "fieldtype": "Data",
                "insert_after": "e_invoice_section_break",
                "label": "Activity Code",
                "fetch_if_empty": 1,
                "allow_on_submit": 1,
                "fetch_from": "company.activity_code"
            },
            {
                "fieldname": "branch",
                "fieldtype": "Link",
                "options": "Branches",
                "insert_after": "activity_code",
                "label": "Branch",
                "allow_on_submit": 1,
            },
            {
                "fieldname": "branch_code",
                "fieldtype": "Data",
                "insert_after": "branch",
                "label": "Branch Code",
                "fetch_if_empty": 1,
                "allow_on_submit": 1,
                "fetch_from": "branch.branch_code"
            },
            {
                "fieldname": "date_issued",
                "fieldtype": "Datetime",
                "insert_after": "branch_code",
                "label": "Datetime Issued",
                # "read_only":1
            },
            {
                "fieldname": "datetime_issued",
                "fieldtype": "Data",
                "insert_after": "date_issued",
                "label": "Datetime Issued",
                "read_only": 1
            },
            {
                "fieldname": "taxable_item",
                "fieldtype": "Link",
                "options": "Taxable Items",
                "insert_after": "datetime_issued",
                "label": "Taxable Item",
            },
            {
                "fieldname": "is_send",
                "fieldtype": "Check",
                "insert_after": "taxable_item",
                "label": "Is Send",
                "read_only": 1
            },
            {
                "fieldname": "e_invoice_status_section_break",
                "fieldtype": "Section Break",
                "insert_after": "is_send",
                "label": "Submission Status"
            },
            {
                "fieldname": "inv_status",
                "fieldtype": "Select",
                "options": "\nSubmitted\nValid\nInvalid\nCancelled",
                "label": "Invoice Status",
                "insert_after": "e_invoice_status_section_break",
                "in_filter": 1,
                "in_standard_filter": 1,
                "in_list_view": 1,
                "read_only": 1,
                "allow_on_submit": 1,
            },
            {
                "fieldname": "error_details_column",
                "fieldtype": "Column Break",
                "label": "Error",
                "insert_after": "e_invoice_status_section_break",
                # "read_only":1,
                # "allow_on_submit":1,
            },
            {
                "fieldname": "error_code",
                "fieldtype": "Data",
                "label": "Error Code",
                "insert_after": "error_details_column",
                "read_only": 1,
                "allow_on_submit": 1,
            },
            {
                "fieldname": "error_details",
                "fieldtype": "Text",
                "label": "Error Details",
                "insert_after": "error_code",
                "read_only": 1,
                "allow_on_submit": 1,
            },

        ],
        'Sales Invoice Item': [

            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "description",
                "label": "",
            },

            {
                "fieldname": "item_type",
                "fieldtype": "Select",
                "fetch_if_empty": 1,
                "options": "GS1\nEGS",
                "fetch_from": "item_code.item_type",
                "insert_after": "e_invoice_section_break",
                "label": "Item Type",
            },
            {
                "fieldname": "itemcode",
                "fieldtype": "Data",
                "fetch_if_empty": 1,
                "fetch_from": "item_code.itemcode",
                "insert_after": "item_type",
                "label": "ItemCode",
            },

            {
                "fieldname": "e_invoice_column_break",
                "fieldtype": "Column Break",
                "insert_after": "itemcode",
                "label": "",
            },
            {
                "fieldname": "tax_rate",
                "fieldtype": "Float",
                "insert_after": "e_invoice_column_break",
                "label": "Tax Rate",
                "default": 0,
                "reqd": 0,
            },
            {
                "fieldname": "tax_amount",
                "fieldtype": "Float",
                "insert_after": "tax_rate",
                "label": "Tax Amount",
                "default": 0,
                # "reqd": 1,
            },

        ],
        'Item Tax Template Detail': [
            {
                "fieldname": "tax_type_invoice",
                "fieldtype": "Link",
                "insert_after": "tax_type",
                "label": "Tax Type Invoice",
                "options": "Tax Types",
                "in_list_view": 1
            },
            {
                "fieldname": "tax_sub_type",
                "fieldtype": "Link",
                "insert_after": "tax_type_invoice",
                "label": "Tax Sub Type",
                "options": "Tax Types",
                "in_list_view": 1
            },
            {
                "fieldname": "amount",
                "fieldtype": "Float",
                "insert_after": "tax_rate",
                "label": "Amount",
                "in_list_view": 1,
                "default": 0
            },
        ],
        'Sales Taxes and Charges':[

            {
                "fieldname": "tax_type",
                "fieldtype": "Link",
                "options":"Tax Types",
                "insert_after": "account_head",
                "label": "Tax Type",
                "allow_on_submit": 1
            },
            {
                "fieldname": "tax_subtype",
                "fieldtype": "Link",
                "options":"Tax Types",
                "insert_after": "account_head",
                "label": "Tax Type",
                "allow_on_submit": 1
            },
        ]
    },
    "properties":

        [
            {
                "doc_type": "Customer",
                "field_name": "tax_id",
                "property": "label",
                "property_type": "Data",
                "value": "ID",
                "doctype_or_field": "DocField",
            }
    ],

    'on_setup': 'dynamic.e_invoice.setup.install_e_invoice'
}
