# Copyright (c) 2013, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext import get_company_currency, get_default_company
def execute(filters=None):
	columns, data =get_columns(filters), get_data(filters)
	return columns, data


def get_balance(row, balance, debit_field, credit_field):
	balance += (row.get(debit_field, 0) -  row.get(credit_field, 0))

	return balance

def get_result_as_list(data, filters):
	balance, balance_in_account_currency = 0, 0
	
	for d in data:
		if not d.get('posting_date'):
			balance, balance_in_account_currency = 0, 0

		balance = get_balance(d, balance, 'debit', 'credit')
		d['balance'] = balance

		
		
	return data



def get_data(filters=None):
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date must be before To Date"))
	gl_type=  filters.get("account_type") 
	accounts = f""" (select name from `tabAccount` WHERE account_type = '{gl_type}' )"""
	if filters.get("mode_of_payment") :
		accounts =f""" (SELECT default_account FROM 
							`tabMode of Payment Account` WHERE parent = '{filters.get("mode_of_payment")}' )"""
	
	date_qyery = f"""  AND posting_date between date('{filters.from_date }')  AND  date('{filters.to_date }') """
	sql_qery = f"""SELECT name as gl_entry , posting_date ,account , debit ,credit ,0 as balance  ,voucher_type 
				FROM `tabGL Entry`  
				 WHERE account in {accounts}
	   """ +date_qyery
	data = frappe.db.sql(sql_qery ,as_dict=1)
	return (get_result_as_list(data , filters) )

def get_columns(filters=None) :
	currency = get_company_currency(filters["company"]) if filters else get_default_company()
	columns = [
		{
			"label": _("GL Entry"),
			"fieldname": "gl_entry",
			"fieldtype": "Link",
			"options": "GL Entry",
			"hidden": 1
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width":130
		},
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			"width":270
		},
		{
			"label": _("Debit ({0})".format(currency)),
			"fieldname": "debit",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Credit ({0})".format(currency)),
			"fieldname": "credit",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Balance ({0})".format(currency)),
			"fieldname": "balance",
			"fieldtype": "Float",
			"width": 130
		},
			{
			"label": _("Voucher Type"),
			"fieldname": "voucher_type",
			"width": 180
		},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180
		},
			
	]
	return columns