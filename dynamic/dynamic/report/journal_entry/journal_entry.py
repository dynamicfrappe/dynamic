# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data

def get_data():
	sql = f'''
			select 
				j.name ,ja.account ,ja.debit_in_account_currency , ja.credit_in_account_currency , ja.cost_center 
			from
				`tabJournal Entry Account` ja
			inner join
				`tabJournal Entry` j
			on
				ja.parent = j.name
			'''
	data = frappe.db.sql(sql , as_dict = 1)
	return data
	
def get_columns():
	return [
		{
			"label": _("Journal Entry"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Journal Entry",
			"width":200

		},
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width":200

		},
		{
			"label": _("Debit"),
			"fieldname": "debit_in_account_currency",
			"fieldtype": "Currency",
			"options": "currency",
			"width":150

		},
		{
			"label": _("Credit"),
			"fieldname": "credit_in_account_currency",
			"fieldtype": "Currency",
			"options": "currency",
			"width":150

		},
		{
			"label": _("Cost Center"),
			"fieldname": "cost_center",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width":150

		},
	]