from __future__ import unicode_literals

data = {

    'custom_fields': {},
    "properties":[
                        {
                        "doc_type": "Journal Entry Account",
                        "doctype_or_field": "DocField",
                        "field_name": "reference_type",
                        "name": "Journal Entry Account-reference_type-options",
                        "property": "options",
                        "property_type": "Text",
                        "value": ["Sales Invoice","Purchase Invoice","Journal Entry","Sales Order","Purchase Order","Expense Claim","Asset","Loan","Payroll Entry","Employee Advance","Exchange Rate Revaluation","Invoice Discounting","Fees","Pay and Receipt Document"]
                        }
                ],
     "property_setters": [ 
        {
        "doc_type": "Journal Entry Account",
        "doctype_or_field": "DocField",
        "field_name": "reference_type",
        "name": "Journal Entry Account-reference_type-options",
        "property": "options",
        "property_type": "Text",
        "value": ["Sales Invoice","Purchase Invoice","Journal Entry","Sales Order","Purchase Order","Expense Claim","Asset","Loan","Payroll Entry","Employee Advance","Exchange Rate Revaluation","Invoice Discounting","Fees","Pay and Receipt Document"]
        }
                        ],
    'on_setup': 'dynamic.dynamic_accounts.setup.install_dynamic_accounts'
}
