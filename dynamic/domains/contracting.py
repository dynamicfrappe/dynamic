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
                            "fieldname": "is_contracting",
                            "fieldtype": "Check",
                            "insert_after": "schedule_date",
                            "label": "Has Clearence",

                        },

                        {
                            "depends_on": "eval:doc.is_contracting==\"1\"",
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
                            "fieldname": "is_contracting",
                            "fieldtype": "Check",
                            "insert_after": "delivery_date",
                            "label": "Has Clearence",

                        },
                        {
                             "depends_on": "eval:doc.is_contracting==\"1\"",
                            "fieldname": "comparison",
                            "fieldtype": "Link",
                            "insert_after": "is_contracting",
                            "label": "Comparison",
                            "options":"Comparison"

                        },
                        
                        {
                             "depends_on": "eval:doc.is_contracting==\"1\"",
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

                        }


                    ] ,
        'Stock Entry' :
                    [
                        {
                            "fieldname": "against_comparison",
                            "fieldtype": "Check",
                            "insert_after": "stock_entry_type",
                            "depends_on":"eval:doc.stock_entry_type=='Material Issue'",
                            "label": "Against Comparison",

                        },
                        {
                            "fieldname": "comparison",
                            "fieldtype": "Link",
                            "insert_after": "against_comparison",
                            "options" : "Comparison",
                            "depends_on":"eval:doc.against_comparison == 1",
                            "mandatory_depends_on":"eval:doc.against_comparison == 1",
                            "label": "Comparison",

                        }
                    ],



        'Stock Entry Detail' :
                    [

                        {
                            "fieldname": "comparison_item",
                            "fieldtype": "Link",
                            "insert_after": "item_name",
                            "options" : "Item",
                            "label": "Against Item",
                        },
                        {
                            "fieldname": "comparison_item_name",
                            "fieldtype": "Data",
                            "read_only" : 1 ,
                            "insert_after": "comparison_item",
                            "fetch_from" : "comparison_item.item_name",
                            "label": "Against Item Name",
                        }
                    ]

      },

    'on_setup': 'dynamic.contracting.add_client_Sccript.add_sales_order_script'
    }