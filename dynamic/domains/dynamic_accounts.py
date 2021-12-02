from __future__ import unicode_literals

data = {

    'custom_fields': {},
    "properties":[
        {
            "doc_type": "Journal Entry Account",
            "doctype_or_field":"DocField",
            "field_name": "reference_type",
            "property": "options",
            "property_type": "Text",
            "value": "\nSales Invoice\nPurchase Invoice\nJournal Entry\nSales Order\nPurchase Order\nExpense Claim\nAsset\nLoan\nPayroll Entry\nEmployee Advance\nExchange Rate Revaluation\nInvoice Discounting\nFees\nPay and Receipt Document"
        }
    ],
    'on_setup': 'dynamic.dynamic_accounts.setup.install_dynamic_accounts'
}