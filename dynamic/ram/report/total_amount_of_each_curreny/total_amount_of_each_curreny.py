# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_column(), get_data(filters)
	return columns, data

def get_data(filters):
	conditions = ' and 1=1'
	# if filters.get("currency"):
	# 	conditions += f' and a.account_currency = "{filters.get('currency')}"'
	# if filters.get("account_type"):
	# 	conditions += f' and a.account_type = "{filters.get('account_type')}"'

	sql = f'''
			select 
				a.account_currency , a.account_type , p.paid_to , sum(p.paid_amount) as sum , p.mode_of_payment
			from 
				`tabAccount` a
			inner join 
				`tabPayment Entry` p
			where 
				p.paid_to = a.name
				and
				(a.account_type ="Bank" or a.account_type =  "Cash")
				and
				a.account_currency =  p.paid_to_account_currency
				and 
				p.status = 'Submitted'
				{conditions}
			group by 
				a.account_currency , a.account_type
		'''
	data = frappe.db.sql(sql , as_dict = 1)
	return data 

def get_column():
	return [
            {
                "label": _("Currency"),
                "fieldname": "account_currency",
                "fieldtype": "Link",
                "options": "Currency",
                "width": 180,
            },
            {
                "label": _("Account Type"),
                "fieldname": "account_type",
                "fieldtype": "Data",
                "width": 180,
            },
            {
                "label": _("Paid Amount"),
                "fieldname": "sum",
                "fieldtype": "Float",
                "width": 180,
            },
			{
                "label": _("Mode of Payment"),
                "fieldname": "mode_of_payment",
                "fieldtype": "Link",
                "options": "Mode of Payment",
                "width": 180,
            },
			]
