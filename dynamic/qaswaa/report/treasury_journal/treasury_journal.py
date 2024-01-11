# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.utils import get_balance_on
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_data(filters):
	conditions = " 1=1"
	if filters.get("mode_of_payment"):	
		result_string = str(filters.get("mode_of_payment")).replace('[', '(').replace(']', ')')
		conditions += f" and P.name in {result_string} "

	sql = f'''
	 	SELECT
	  		default_account
		FROM
		  `tabMode of Payment` P
		INNER JOIN 
			`tabMode of Payment Account` PA
		ON 
			P.name = PA.parent
		WHERE
			{conditions}
		'''
	data = frappe.db.sql(sql , as_dict = 1)
	if not data :
		frappe.throw(_("Select <b>account</b> in mode of payment"))
	gl_conditions = " 1=1"
	if filters.get("from_date"):
		gl_conditions += f" and posting_date >= '{filters.get('from_date')}'"
	if filters.get("to_date"):
		gl_conditions += f" and posting_date <= '{filters.get('to_date')}'"
	accounts = []
	for entry in data :
		accounts.append(entry["default_account"])
	account_list = tuple(accounts)
	if not len(account_list) > 1 :
		account_list = f" ('{str(account_list[0]).replace(',', '')}' )"

	s = f'''
			SELECT
				account , posting_date , voucher_no , against 
				, remarks , debit , credit 
			FROM
				`tabGL Entry` P
			WHERE
				{gl_conditions}
				and 
				account in {account_list} 
				and 
				voucher_type = "Payment Entry"
			ORDER BY 
				credit 
		'''
	gl_entries = frappe.db.sql(s , as_dict = 1)
	for gl_entry in gl_entries:
		gl_entry["balance"] = get_balance_on (account =f'{gl_entry["account"]}' ,date =f'{gl_entry["posting_date"]}')
	return gl_entries
	
def get_columns():
	columns = [
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width": 250,
		},
		{
			"fieldname": "posting_date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 300,
		},
		{
			"label": _("Payment Entry"),
			"fieldname": "voucher_no",
			"fieldtype": "Link",
			"options": "Payment Entry",
			"width": 250,
		},
		{
			"label": _("Against"),
			"fieldname": "against",
			"fieldtype": "Text",
			"width": 250,
		},
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Text",
			"width": 250,
		},
		{
			"fieldname": "debit",
			"label": "Debit",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "credit",
			"label": "Credit",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "balance",
			"label": "Balance",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		}
	]
	return columns
