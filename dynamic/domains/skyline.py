from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    'custom_fields': {
        "Project": 
        [
            {
                "label": "Revised contract amount",
                "fieldname": "revised_contract_amount",
                "fieldtype": "Table",
                "options" : "Contract Amount",
                "insert_after": "project_warehouse",
            },
            {
                "label": "Variation order",
                "fieldname": "total_contracts",
                "fieldtype": "Float",
                "insert_after": "revised_contract_amount",
                "read_only": "1",
            },
            {
                "label": "Contract amount",
                "fieldname": "contract_amounts",
                "fieldtype": "Float",
                "insert_after": "sales_order",
            },
            {
                "label": "Final contract amount",
                "fieldname": "total_contract_amountt",
                "fieldtype": "Float",
                "insert_after": "contract_amounts",
                "read_only": "1",
            },
            ##########
            {
                "label": "Invoice and Paid amount",
                "fieldname": "invoice_amounts_sec",
                "fieldtype": "Section Break",
                "insert_after": "total_contract_amountt",
                "collapsible ":1 
            },
            {
                "label": "Invoice amount",
                "fieldname": "invoice_amounts",
                "fieldtype": "Table",
                "options" : "Contract Amount",
                "insert_after": "invoice_amounts_sec",
            },
            {
                "label": "Total invoice amount",
                "fieldname": "total_invoice_amount",
                "fieldtype": "Float",
                "insert_after": "invoice_amounts",
                "read_only": "1",
            },
            {
                "label": "Paid amount",
                "fieldname": "paid_amounts",
                "fieldtype": "Table",
                "options" : "Paid Amount",
                "insert_after": "total_invoice_amount",
            },
            {
                "label": "Total paid amount",
                "fieldname": "total_paid_amount",
                "fieldtype": "Float",
                "insert_after": "paid_amounts",
                "read_only": "1",
            },
            {
                "label": "Difference",
                "fieldname": "diff",
                "fieldtype": "Float",
                "insert_after": "total_paid_amount",
                "read_only": "1",
            },
            #################
            {
                "label": "Cost",
                "fieldname": "cost_sec",
                "fieldtype": "Section Break",
                "insert_after": "diff",
                "collapsible ":1 
            },
            {
                "label": "Original Budget",
                "fieldname": "original_budget",
                "fieldtype": "Currency",
                "insert_after": "cost_sec",
            },
            {
                "label": "Budget Zero",
                "fieldname": "budget_zero",
                "fieldtype": "Currency",
                "insert_after": "original_budget",
            },
           
            {
                "label": "Total",
                "fieldname": "total_rcb",
                "fieldtype": "Float",
                "insert_after": "budget_zero",
            },
            {
                "label": "Estimated Cost",
                "fieldname": "estimated_cost",
                "fieldtype": "Currency",
                "insert_after": "total_rcb",
            },
            {
                "label": "Purchase Order Cost",
                "fieldname": "purchase_order_cost",
                "fieldtype": "Currency",
                "insert_after": "estimated_cost",
            },
            {
                "label": "Payments",
                "fieldname": "payments",
                "fieldtype": "Currency",
                "insert_after": "purchase_order_cost",
            },
        ],
    },
}
