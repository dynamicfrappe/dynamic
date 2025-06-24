import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def safely_create_custom_fields():
    custom_fields = {
        'Lead': [
            {
                "fieldname": "phone_no",
                "fieldtype": "Data",
                "in_global_search": 1,
                "in_standard_filter": 1,
                "insert_after": "email_id",
                "label": "Phone No",
                "translatable": 1,
                "unique": 1,
                "reqd": 1
            }
        ],
        'Customer': [
            {
                "fieldname": "phone_no",
                "fieldtype": "Data",
                "in_global_search": 1,
                "in_standard_filter": 1,
                "insert_after": "sku",
                "label": "Phone No",
                "translatable": 1,
                "unique": 1,
                "fetch_if_empty": 1,
                "fetch_from": "lead_name.phone_no",
                "reqd": 1
            }
        ],
           'Quotation' :[  
            {
                "label": "total advance",
                "fieldname": "total_advance",
                "fieldtype": "Currency",
                "insert_after": "lost_reasons",
            },
            {
                "label": "party account currency",
                "fieldname": "party_account_currency",
                "fieldtype": "Data",
                "insert_after": "total_advance",
            },
            {
                "label": "write off amount",
                "fieldname": "write_off_amount",
                "fieldtype": "Currency",
                "insert_after": "party_account_currency",
                "default": 0,
            },
            {
                "label": "base write off amount",
                "fieldname": "base_write_off_amount",
                "fieldtype": "Data",
                "insert_after": "write_off_amount",
                
            },
           ],
            
        'Opportunity': [
            {
                "fieldname": "info_data",
                "fieldtype": "Section Break",
                "insert_after": "expected_closing",
                "label": "Info Data"
            },
            {
                "fieldname": "customer",
                "fieldtype": "Link",
                "insert_after": "source",
                "label": "Customer",
                "options": "Customer",
                "read_only": 1
            },
            {
                "fieldname": "phone_no",
                "fieldtype": "Data",
                "in_global_search": 1,
                "in_standard_filter": 1,
                "insert_after": "customer",
                "label": "Phone No",
                "translatable": 1,
                "fetch_if_empty": 1,
                "reqd": 1,
                "fetch_from": "party_name.phone_no"
            },
            {
                "label": "Cost Center",
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "insert_after": "phone_no",
                "options": "Cost Center",
                "read_only": 0,
                "allow_on_submit": 0,
                "reqd": 1
            },
            {
                "label": "Opportunity Name",
                "fieldname": "opportunity_name",
                "fieldtype": "Data",
                "insert_after": "customer_name",
                "in_global_search": 1
            }
        ]
    }
    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": doctype,
                    **field
                }).insert()

    frappe.clear_cache()

# نداء الدالة
safely_create_custom_fields()