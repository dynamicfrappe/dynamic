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
		payment_query = f'''
							SELECT 
								payment_type , mode_of_payment ,
								party_type , party_name , paid_amount
							FROM
								`tabPayment Entry`
							WHERE 
								name = '{gl_entry["voucher_no"]}'
 							'''
		payment_details = frappe.db.sql(payment_query , as_dict = 1)
		gl_entry["payment_type"] = payment_details[0]["payment_type"]
		gl_entry["mode_of_payment"] = payment_details[0]["mode_of_payment"]
		gl_entry["party_type"] = payment_details[0]["party_type"]
		gl_entry["party_name"] = payment_details[0]["party_name"]
		gl_entry["paid_amount"] = payment_details[0]["paid_amount"]

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
			"label": _("Payment Type"),
			"fieldname": "payment_type",
			"fieldtype": "Data",
			"width": 250,
		},
		{
			"label": _("Mode of Payment"),
			"fieldname": "mode_of_payment",
			"fieldtype": "Link",
			"options": "Mode of Payment",
			"width": 250,
		},
		{
			"label": _("Party Type"),
			"fieldname": "party_type",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 250,
		},
		{
			"label": _("Party Name"),
			"fieldname": "party_name",
			"fieldtype": "Dynamic Link",
			"options": "party_type",
			"width": 250,
		},
		{
			"fieldname": "paid_amount",
			"label": "Paid Amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150,
		},
		{
			"fieldname": "posting_date",
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"width": 300,
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
