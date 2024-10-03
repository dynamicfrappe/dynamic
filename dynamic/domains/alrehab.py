from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    'custom_fields': {
        'Customer':[
            {
                "label":_("Owner Name"),
                "fieldname":"owner_name",
                "fieldtype":"Link",
                "options":"Owner",
                "insert_after":"customer_type",  
            },   
            {
                "label":_("Commercial year"),
                "fieldname":"commercial_year",
                "fieldtype":"Link",
                "options":"Commercial year",
                "insert_after":"owner_name",  
            },     
            # Unit area
            {
                "label":_("Unit area"),
                "fieldname":"unit_area",
                "fieldtype":"Data",
                "insert_after":"commercial_year",  
            },  
            {
                 "label":_("Building Number"),
                "fieldname":"building_number",
                "fieldtype":"Data",
                "insert_after":"unit_area", 
            }

        ],
        'Journal Entry':[
            {
                "label":_("installment Entry"),
                "fieldname":"installment_entry",
                "fieldtype":"Link",
                "options":"installment Entry",
                "insert_after":"tax_withholding_category", 
            },
        ],
        'Subscription':[
            {
                "fieldname":"sec_deferred_revenue",
                "fieldtype":"Section Break",
                "insert_after":"dimension_col_break", 
                "collapsible ":1 
            },
            {
                "label":_("Deferred Revenue Amount"),
                "fieldname":"deferred_revenue_amount",
                "fieldtype":"Currency",
                "insert_after":"sec_deferred_revenue", 
                "read_only": 1,
            },
            {
                "label":_("Penalty"),
                "fieldname":"penalty",
                "fieldtype":"Float",
                "insert_after":"plans",
                "reqd": 1,
            },
        ],
        'Company':[
            {
                "fieldname":"sec_dc_accounts",
                "fieldtype":"Section Break",
                "insert_after":"default_discount_account", 
            },
            {
                "label":_("Debit Account"),
                "fieldname":"debit_account",
                "fieldtype":"Link",
                "options":"Account",
                "insert_after":"sec_dc_accounts", 
            },
            {
                "fieldname": "col_break_cd_acc",
                "fieldtype": "Column Break",
                "insert_after": "debit_account",
            },
            {
                "label":_("Credit Account"),
                "fieldname":"credit_account",
                "fieldtype":"Link",
                "options":"Account",
                "insert_after":"col_break_cd_acc", 
            },
        ],
        'Sales Invoice':[
            {
                "label": "الغرامات",
                "fieldname":"sec_fines",
                "fieldtype":"Section Break",
                "insert_after":"items", 
            },
            {
                "label": "نسبة الغرامة",
                "fieldname":"fine_percent",
                "fieldtype":"Float",
                "insert_after":"sec_fines",
                "read_only": 1,
            },
            {
                "fieldname": "col_break_01",
                "fieldtype": "Column Break",
                "insert_after": "fine_percent",
            },
            {
                "label": "أيام التأخير",
                "fieldname":"num_of_delay_days",
                "fieldtype":"Int",
                "insert_after":"col_break_01",
                "read_only": 1,
            },
            {
                "fieldname": "col_break_02",
                "fieldtype": "Column Break",
                "insert_after": "num_of_delay_days",
            },
            {
                "label": "مبلغ الغرامة",
                "fieldname":"deferred_revenue_amount",
                "fieldtype":"Currency",
                "insert_after":"col_break_02", 
                "read_only": 1,
            },
            {
                "label": "Payment Date",
                "fieldname":"payment_actual_due_date",
                "fieldtype":"Date",
                "insert_after":"due_date", 
            },
            {
                "label": "Get Updates",
                "fieldname":"get_update_btn",
                "fieldtype":"Button",
                "insert_after":"deferred_revenue_amount", 
                "allow_on_submit":1
            },
        ],
        
    },
    "properties": [
        {
        "doctype": "Journal Entry",
        "doctype_or_field": "DocField",
        "fieldname": "installment_entry",
        "property": "read_only",
        "property_type": "Check",
        "value": "1",
        },
        {
        "doctype": "Subscription Plan Detail",
        "doctype_or_field": "DocField",
        "fieldname": "qty",
        "property": "label",
        "property_type": "data",
        "value": "Area",
        },
    ],
  
   'on_setup': 'dynamic.alrehab.setup.install_elrehab'
}