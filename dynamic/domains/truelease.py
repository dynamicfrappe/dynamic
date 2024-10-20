
from __future__ import unicode_literals

data = {

    'custom_fields': {
      'Lead': [
         {
            "label" :"Sector" ,
            "fieldname": "sector",
            "fieldtype": "Link",
            "insert_after": "status",
            "options" :"Industry Type", 
         },
         {
            "label" :"Sales -mm- EGP" ,
            "fieldname": "sales_mm_egp",
            "fieldtype": "Float",
            "insert_after": "sector",
         },
         {
            "label" :"Dealing Banks" ,
            "fieldname": "dealing_banks",
            "fieldtype": "Data",
            "insert_after": "sales_mm_egp",
         },
         {
            "label": "Phone no",
            "fieldname": "phone_num",
            "fieldtype": "Data",
            "insert_after": "email_id",
         },
         {
            "label" :"Government" ,
            "fieldname": "government",
            "fieldtype": "Data",
            "insert_after": "phone_no",
         },
         {
            "label" :"Client Profile Status" ,
            "fieldname": "cp_status",
            "fieldtype": "Select",
            "insert_after": "status",
            "options": "\nApproved\nRejected"
         }
      ],
      'Actions': [
         {
            "label" :"Sub Actions" ,
            "fieldname": "sub_actions",
            "fieldtype": "Select",
            "insert_after": "action",
            "options": "\nNew\nExisted\nAnnual Review",
         },
         {
            "label" :"Approval: " ,
            "fieldname": "approval",
            "fieldtype": "Link",
            "insert_after": "type",
            "options" :"User", 
         },
         {
            "label" :"Approved By: " ,
            "fieldname": "approved_by",
            "fieldtype": "Data",
            "insert_after": "approval",
         },
         {
            "label" :"Status: " ,
            "fieldname": "status",
            "fieldtype": "Select",
            "insert_after": "approved_by",
            "options" :"Draft\nApproved\nRejected", 
         },
         {
            "label" :"Status By Department: " ,
            "fieldname": "status_depart",
            "fieldtype": "Select",
            "insert_after": "action_name",
            "options" :"\nPending\nDone", 
         },
         {
            "label" :"Organization: " ,
            "fieldname": "org_name",
            "fieldtype": "Data",
            "insert_after": "customer",
            "fetch_from": "customer.company_name"
         },
         {
            "fieldname": "attachments_section",
            "fieldtype": "Section Break",
            "insert_after": "created_by",
         },
         {
            "label" :"Customer Table with Attachments" ,
            "fieldname": "customer_table_with_attachments",
            "fieldtype": "Table",
            "insert_after": "attachments_section",
            "options" :"Customer Table with Attachments", 
         },
         {
            "label": "Department",
            "fieldname": "department",
			   "fieldtype": "Link",
			   "options": "Departments",
			   "insert_after": "create_by",
         },
         {
            "label": "Amended From",
            "fieldname": "amended_from",
            "fieldtype": "Link",
            "insert_after": "create_by",
            "no_copy": 1,
            "options": "Actions",
            "print_hide": 1,
            "read_only": 1
         }
      ],
      'Quotation': [
         {
            "label" :"Lessee" ,
            "fieldname": "lessee",
            "fieldtype": "Data",
            "insert_after": "company",
         },
         {
            "label" :"Lease Description" ,
            "fieldname": "lease_description",
            "fieldtype": "Data",
            "insert_after": "lessee",
         },
         {
            "fieldname": "lease_section",
            "fieldtype": "Section Break",
            "insert_after": "order_type",
         },
         {
            "label" :"Assets" ,
            "fieldname": "assets",
            "fieldtype": "Data",
            "insert_after": "lease_section",
         },
         {
            "label" :"Net financed Amount" ,
            "fieldname": "net_financed_amount",
            "fieldtype": "Data",
            "insert_after": "assets",
         },
         {
            "label" :"Percent of Finance" ,
            "fieldname": "percent_of_finance",
            "fieldtype": "Data",
            "insert_after": "net_financed_amount",
         },
         {
            "label" :"Tenor" ,
            "fieldname": "tenor",
            "fieldtype": "Data",
            "insert_after": "percent_of_finance",
         },
         {
            "label" :"Installements" ,
            "fieldname": "installements",
            "fieldtype": "Currency",
            "insert_after": "percent_of_finance",
         },
         {
            "fieldname": "cbreak",
            "fieldtype": "Column Break",
            "insert_after": "installements",
         },
         {
            "label" :"Reserve" ,
            "fieldname": "reserve",
            "fieldtype": "Data",
            "insert_after": "cbreak",
         },
         {
            "label" :"Payment Method" ,
            "fieldname": "payment_method",
            "fieldtype": "Data",
            "insert_after": "reserve",
         },
         {
            "label" :"Use of Fund" ,
            "fieldname": "use_of_fund",
            "fieldtype": "Data",
            "insert_after": "payment_method",
         },
         {
            "label" :"Arrangement Fee" ,
            "fieldname": "arrangement_fee",
            "fieldtype": "Data",
            "insert_after": "use_of_fund",
         },
      ],
      'User':[
         {
            "label" :"Department" ,
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Departments",
            "insert_after": "username",
         }
      ]
    },
     "properties": [
      #  Lead
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "salutation",
        "property": "hidden",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "designation",
        "property": "hidden",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "fax",
        "property": "hidden",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "address_type",
        "property": "hidden",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "more_info",
        "property": "hidden",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "campaign_name",
        "property": "hidden",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "organization_lead",
        "property": "default",
        "property_type": "Data",
        "value": "1"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "lead_name",
        "property": "label",
        "property_type": "Data",
        "value": "Name"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocType",
        "property": "autoname",
        "property_type": "Data",
        "value": "field:company_name"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "status",
        "property": "default",
        "property_type": "Small Text",
        "value": "Open"
        },
        {
        "doctype": "Lead",
        "doctype_or_field": "DocField",
        "fieldname": "status",
        "property": "options",
        "property_type": "Select",
        "value": "Open\nOpportunity\nClose"
        },
        
      #  Actions
        {
        "doctype": "Actions",
        "doctype_or_field": "DocType",
        "property": "is_submittable",
        "property_type": "Check",
        "value": "1"
        },
        {
        "doctype": "Actions",
        "doctype_or_field": "DocField",
        "fieldname": "type",
        "property": "options",
        "property_type": "Select",
        "value": "Call\nVisit"
        },
        {
        "doctype": "Actions",
        "doctype_or_field": "DocField",
        "fieldname": "phone_no",
        "property": "fetch_from",
        "property_type": "Data",
        "value": "customer.phone_num"
        },
        
        {
        "doctype": "Actions",
        "doctype_or_field": "DocField",
        "fieldname": "action",
        "property": "fieldtype",
        "property_type": "Select",
        "value": "Data"
        },
      #  Action
        {
        "doctype": "Action",
        "doctype_or_field": "DocField",
        "fieldname": "type",
        "property": "options",
        "property_type": "Select",
        "value": "Call\nVisit"
        },
      #  Quotation
        {
        "doctype": "Quotation",
        "doctype_or_field": "DocField",
        "fieldname": "company",
        "property": "label",
        "property_type": "Data",
        "value": "Lessor"
        },
        {
        "doctype": "Quotation",
        "doctype_or_field": "DocField",
        "fieldname": "order_type",
        "property": "reqd",
        "property_type": "Check",
        "value": 0
        },
        {
        "doctype": "Quotation",
        "doctype_or_field": "DocField",
        "fieldname": "order_type",
        "property": "hidden",
        "property_type": "Check",
        "value": 1
        },
        {
        "doctype": "Quotation",
        "doctype_or_field": "DocField",
        "fieldname": "items",
        "property": "reqd",
        "property_type": "Check",
        "value": 0
        },
        {
        "doctype": "Quotation",
        "doctype_or_field": "DocField",
        "fieldname": "items",
        "property": "hidden",
        "property_type": "Check",
        "value": 1
        },
     ]
}
