from __future__ import unicode_literals
from frappe import _


data = {

    'custom_fields': {
       "Company":[
        {
            "fieldname":"company_arabic_name",
            "fieldtype":"Data",
            "insert_after":"company_name",
            "label":"Company Arabic Name",
        }
       ],
       'Sales Order':[
            {
                "label": "Advance Payment",
                "fieldname": "advance_paymentss",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule"
            },
            {
                "label": "Get Advances Receivedd",
                "fieldname": "get_advancess",
                "fieldtype": "Button",
                "insert_after": "advance_paymentss",
                "allow_on_submit":1
            },
            {
                "label": "Advances",
                "fieldname": "advancess",
                "fieldtype": "Table",
                "options":"Sales Invoice Advance",
                "insert_after": "get_advancess",
                "allow_on_submit":1
            },
            {
                "label": _("Outstanding Amount"),
                "fieldname": "outstanding_amount",
                "fieldtype": "Float",
                "insert_after": "advance_paid",
                "allow_on_submit":1,
                "read_only" : 1
            },
             
         ],
         'Quotation':[
            {
                "label": "Advance Payment",
                "fieldname": "advance_paymentss",
                "fieldtype": "Section Break",
                "insert_after": "payment_schedule"
            },
            {
                "label": "Get Advances Receivedd",
                "fieldname": "get_advancess",
                "fieldtype": "Button",
                "insert_after": "advance_paymentss",
                "allow_on_submit":1
            },
            {
                "label": "Advances",
                "fieldname": "advancess",
                "fieldtype": "Table",
                "options":"Sales Invoice Advance",
                "insert_after": "get_advancess",
                "allow_on_submit":1
            },  
            {
                "label": _("Outstanding Amount"),
                "fieldname": "outstanding_amount",
                "fieldtype": "Float",
                "insert_after": "in_words",
                "allow_on_submit":1,
                "read_only" : 1
            },  
            
         ],
         
    },
    "properties": [{
        # "doctype":"Journal Entry Account",
        # "doctype_or_field":"DocField",
        # "fieldname":"reference_type",
        # "property":"options",
        # "property_type":"Text",
        # "value": "\nSales Invoice\nPurchase Invoice\nJournal Entry\nSales Order\nPurchase Order\nExpense Claim\nAsset\nLoan\nPayroll Entry\nEmployee Advance\nExchange Rate Revaluation\nInvoice Discounting\nFees\nComparison\nClearance\nTender\nPayroll Month\nCheque\nPay Document\nReceipt Document\nPayment Entry"
    }],

   'on_setup': 'dynamic.dynamic_accounts.setup.install_dynamic_accounts'
}
