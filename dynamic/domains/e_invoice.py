from __future__ import unicode_literals

data = {
    'custom_fields': {
        'UOM':[
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
        'Customer':[
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
                "options":"P\nB\nF",
                "default":"P",
                "label": "Receiver Type",
                "name": "Customer-receiver_type",
                
                "reqd":1
            },
            {
                "fieldname": "receiver_id",
                "fieldtype": "Data",
                "insert_after": "receiver_type",
                "label": "Receiver ID",
                "name": "Customer-receiver_id",
                "mandatory_depends_on":"eval:doc.receiver_type=='P'"
                # "reqd":1
            },
            {
                "fieldname": "country_code",
                "fieldtype": "Link",
                "insert_after": "receiver_id",
                "label": "Country Code",
                "options":"Country Code",
                "name": "Customer-country_code",
                "reqd":1
            },
            {
                "fieldname": "governate",
                "fieldtype": "Data",
                "insert_after": "country_code",
                "label": "Governate",
                "name": "Customer-governate",
                "reqd":1
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
                "reqd":1
            },
            {
                "fieldname": "street",
                "fieldtype": "Data",
                "insert_after": "regioncity",
                "label": "Street",
                "name": "Customer-street",
                "reqd":1
            },
            {
                "fieldname": "buildingnumber",
                "fieldtype": "Data",
                "insert_after": "street",
                "label": "Building Number",
                "name": "Customer-buildingnumber",
                "reqd":1
            },

        ] ,
        'Company':[
            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "parent_company",
                "label": "E Invoice Address",
                "name": "Company-e_invoice_section_break",
            },
            {
                "fieldname": "issuer_type",
                "fieldtype": "Select",
                "insert_after": "e_invoice_section_break",
                "options":"P\nB\nF",
                "default":"P",
                "label": "Issuer Type",
                "name": "Company-issuer_type",
                
                "reqd":1
            },
            {
                "fieldname": "issuer_id",
                "fieldtype": "Data",
                "insert_after": "issuer_type",
                "label": "Issuer ID",
                "name": "Company-issuer_id",
                "mandatory_depends_on":"eval:doc.issuer_type=='P'"
                # "reqd":1
            },
            {
                "fieldname": "country_code",
                "fieldtype": "Link",
                "insert_after": "issuer_id",
                "label": "Country Code",
                "options":"Country Code",
                "name": "Company-country_code",
                "reqd":1
            },
            {
                "fieldname": "governate",
                "fieldtype": "Data",
                "insert_after": "country_code",
                "label": "Governate",
                "name": "Company-governate",
                "reqd":1
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
                "reqd":1
            },
            {
                "fieldname": "street",
                "fieldtype": "Data",
                "insert_after": "regioncity",
                "label": "Street",
                "name": "Company-street",
                "reqd":1
            },
            {
                "fieldname": "buildingnumber",
                "fieldtype": "Data",
                "insert_after": "street",
                "label": "Building Number",
                "name": "Company-buildingnumber",
                "reqd":1
            },

        ] ,
        'Item':[
             {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "description",
                "label": "",
                "name": "Sales Invoice-e_invoice_section_break"
            },
            {
                "fieldname": "item_type",
                "fieldtype": "Select",
                "insert_after": "e_invoice_section_break",
                "label": "Item Type",
                "options":"GS1\nEGS",
                "name": "Sales Invoice-item_type",
                "in_filter":1,
                "in_standard_filter":1
            },
            {
                "fieldname": "itemcode",
                "fieldtype": "Data",
                "insert_after": "item_type",
                "label": "Item Code",
                "name": "Sales Invoice-itemcode",
                "in_filter":1,
                "in_standard_filter":1
            },
        ],
        'Sales Invoice' : [
            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "cost_center",
                "label": "",
                "name": "Sales Invoice-e_invoice_section_break"
            },
            {
                "fieldname": "tax_auth",
                "fieldtype": "Check",
                "insert_after": "e_invoice_section_break",
                "label": "Tax Auth",
                "name": "Sales Invoice-tax_auth",
                "in_filter":1,
                "in_standard_filter":1
            },
            {
                "fieldname": "date_issued",
                "fieldtype": "Datetime",
                "insert_after": "tax_auth",
                "label": "Datetime Issued",
                "name": "Sales Invoice-date_issued",
                # "read_only":1
            },
            {
                "fieldname": "datetime_issued",
                "fieldtype": "Data",
                "insert_after": "date_issued",
                "label": "Datetime Issued",
                "name": "Sales Invoice-datetime_issued",
                "read_only":1
            },
            {
                "fieldname": "taxable_item",
                "fieldtype": "Link",
                "options":"Taxable Items",
                "insert_after": "datetime_issued",
                "label": "Taxable Item",
                "name": "Sales Invoice-taxable_item"
            },
            
        ] ,
        'Sales Invoice Item' : [

            {
                "fieldname": "e_invoice_section_break",
                "fieldtype": "Section Break",
                "insert_after": "description",
                "label": "",
                "name": "Sales Invoice Item-e_invoice_section_break"
            },
            
            {
                "fieldname": "item_type",
                "fieldtype": "Select",
                "fetch_if_empty":1,
                "options":"GS1\nEGS",
                "fetch_from":"item_code.item_type",
                "insert_after": "e_invoice_section_break",
                "label": "Item Type",
                "name": "Sales Invoice Item-item_type"
            },
            {
                "fieldname": "itemcode",
                "fieldtype": "Data",
                "fetch_if_empty":1,
                "fetch_from":"item_code.itemcode",
                "insert_after": "item_type",
                "label": "ItemCode",
                "name": "Sales Invoice Item-itemcode"
            },

            {
                "fieldname": "e_invoice_column_break",
                "fieldtype": "Column Break",
                "insert_after": "itemcode",
                "label": "",
                "name": "Sales Invoice Item-e_invoice_column_break"
            },
            {
                "fieldname": "tax_rate",
                "fieldtype": "Float",
                "insert_after": "e_invoice_column_break",
                "label": "Tax Rate",
                "default":0,
                "reqd":1,
                "name": "Sales Invoice Item-tax_rate"
            },
            {
                "fieldname": "tax_amount",
                "fieldtype": "Float",
                "insert_after": "tax_rate",
                "label": "Tax Amount",
                "default":0,
                "reqd":1,
                "name": "Sales Invoice Item-tax_amount"
            },
            
        ] ,

},
"properties":

        [
           {
            "doc_type": "Customer",
            "field_name": "tax_id",
            "property": "label",
            "property_type": "Data",
            "value": "ID",
            "doctype_or_field":"DocField",
            }
        ],
    

  
'on_setup': 'dynamic.e_invoice.setup.install_e_invoice'
}