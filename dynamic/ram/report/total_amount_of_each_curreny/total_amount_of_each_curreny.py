# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_column(), get_data(filters)
	return columns, data

def get_data(filters):
	conditions = ' and 1=1'
	if filters.get("currency"):
		conditions += f' and account.account_currency = "{filters.get("currency")}" '
	if filters.get("account_type"):
		conditions += f' and account.account_type = "{filters.get("account_type")}" '

	sql_query = f'''
        SELECT 
            account.name AS account_name,
            account.parent_account AS parent_account,
            account.account_type AS account_type,
            account.is_group AS is_group,
			account.account_currency , 
            (SELECT SUM( gle.debit - gle.credit)  FROM `tabGL Entry` gle WHERE gle.account = account.name) AS balance,
			(SELECT SUM( gle.debit_in_account_currency - gle.debit_in_account_currency)  FROM `tabGL Entry` gle WHERE gle.account = account.name) AS balance_in_currency
        FROM 
            `tabAccount` account
        WHERE
             account.account_type IN ('Cash', 'Bank')
			 {conditions}
        ORDER BY 
            account.lft ASC;
    '''
	data = frappe.db.sql(sql_query, as_dict=True)
	return data 

def get_column():
	return [
            {
                "label": _("Currency"),
                "fieldname": "account_currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 160,
            },
			{
                "label": _("Account"),
                "fieldname": "account_name",
                "fieldtype": "Link",
                "options": "Account",
                "width": 200,
            },
            {
                "label": _("Account Type"),
                "fieldname": "account_type",
                "fieldtype": "Data",
                "width": 180,
            },
            {
                "label": _("Balance"),
                "fieldname": "balance",
                "fieldtype": "Float",
                "width": 180,
            },
            {
                "label": _("Currency Balance"),
                "fieldname": "balance_in_currency",
                "fieldtype": "Float",
                "width": 180,
            },
			# {
            #     "label": _("Mode of Payment"),
            #     "fieldname": "mode_of_payment",
            #     "fieldtype": "Link",
            #     "options": "Mode of Payment",
            #     "width": 180,
            # },
			]
