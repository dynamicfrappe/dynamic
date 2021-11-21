from __future__ import unicode_literals

data = {
     'custom_fields':
      {
         'Company': [
                        {
                            "fieldname": "contracting",
                            "fieldtype": "Section Break",
                            "insert_after": "date_of_establishment",
                            "label": "Contracting Settings",
                      
                        },
                        {
                            "fieldname": "account_advance_copy_receivable",
                            "fieldtype": "Link",
                            "insert_after": "contracting",
                            "label": "Account Advance Copy Receivable",
                            "options" :"Account"
                      
                        },
                         {
                            "fieldname": "advance_version_account_payable",
                            "fieldtype": "Link",
                            "insert_after": "account_advance_copy_receivable",
                            "label": "Advance Version Account Payable",
                            "options" :"Account"
                      
                        },
                         {
                            "fieldname": "advance_version_account_payable_break",
                            "fieldtype": "Column Break",
                            "insert_after": "advance_version_account_payable",

                        },
                         {
                            "fieldname": "third_party_insurance_account",
                            "fieldtype": "Link",
                            "insert_after": "advance_version_account_payable_break",
                            "label": "Third party insurance account",
                            "options" :"Account"
                      
                        },
                           {
                            "fieldname": "insurance_account_for_others_from_us",
                            "fieldtype": "Link",
                            "insert_after": "third_party_insurance_account",
                            "label": "Insurance Account for others from us",
                            "options" :"Account"
                      
                        },


                    ] ,
         'Purchase Order':[
                        {
                            "fieldname": "contracting",
                            "fieldtype": "Section Break",
                            "insert_after": "ignore_pricing_rule",
                            "label": "Clearance",

                        },
                        {
                            "fieldname": "down_payment_insurance_rate",
                            "fieldtype": "Percent",
                            "insert_after": "contracting",
                            "label": "Down payment insurance rate (%)",

                        },
                        {
                            "fieldname": "advance_version_account_payable_break",
                            "fieldtype": "Column Break",
                            "insert_after": "down_payment_insurance_rate",

                        },
                          {
                            "fieldname": "payment_of_insurance_copy",
                            "fieldtype": "Percent",
                            "insert_after": "advance_version_account_payable_break",
                            "label": "Payment of insurance copy of operation and initial delivery(%)",

                        },


                    ],
        'Sales Order':[
                        {
                            "fieldname": "contracting",
                            "fieldtype": "Section Break",
                            "insert_after": "ignore_pricing_rule",
                            "label": "Clearance",

                        },
                        {
                            "fieldname": "down_payment_insurance_rate",
                            "fieldtype": "Percent",
                            "insert_after": "contracting",
                            "label": "Down payment insurance rate (%)",

                        },
                        {
                            "fieldname": "advance_version_account_payable_break",
                            "fieldtype": "Column Break",
                            "insert_after": "down_payment_insurance_rate",

                        },
                          {
                            "fieldname": "payment_of_insurance_copy",
                            "fieldtype": "Percent",
                            "insert_after": "advance_version_account_payable_break",
                            "label": "Payment of insurance copy of operation and initial delivery(%)",

                        },


                    ]


      }


    }