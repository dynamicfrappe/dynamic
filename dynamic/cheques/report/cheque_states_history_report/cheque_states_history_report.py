# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from datetime import date
import datetime
from frappe.utils import add_to_date
from frappe.utils import getdate
from frappe.utils import pretty_date, now, add_to_date
from erpnext.accounts.utils import get_balance_on
from operator import itemgetter



def execute(filters=None):
	return Cheques_states_history_report(filters).run()


class Cheques_states_history_report(object):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})

	def run(self):
		self.get_columns()
		self.get_data()

		return self.columns , self.data

	def get_columns(self):
		#add columns wich appear data
		self.columns = [
			{
			"fieldname": "Payment",
			"fieldtype": "Link",
			"label": "Payment",
			"options":"Payment Entry",
			"width": 170
		},
			{
			"fieldname": "Cheques NO",
			"fieldtype": "Data",
			"label": "Cheques NO",
			"width": 70

		},
		{
			"fieldname": "Party Type",
			"fieldtype": "Data",
			"label": "Party Type",
			"width": 120
		},
		{
			"fieldname": "Party",
			"fieldtype": "Data",
			"label": "Party",
			"width": 120
		},
		{
			"fieldname": "old_history",
			"fieldtype": "Data",
			"label": "Old History",
			"width": 100

		},
		{
			"fieldname": "Cheque Status",
			"fieldtype": "Data",
			"label": "Cheque Status",
			"width": 120

		},
		{
			"fieldname": "Transaction Date",
			"fieldtype": "Data",
			"label": "Transaction Date",
			"width": 120

		},
		{
			"fieldname": "Reference Date",
			"fieldtype": "Data",
			"label": "Reference Date",
			"width": 120

		},
			{
			"fieldname": "Amount",
			"fieldtype": "Data",
			"label": "Amount",
			"width": 120
		},
		{
			"fieldname": "Bank",
			"fieldtype": "Data",
			"label": "Bank",
			"width": 70
		},
		{
			"fieldname": "Bank Account",
			"fieldtype": "Data",
			"label": "Bank Account",
			"width": 100
		},
		]

		return self.columns


	def get_data(self):
		self.data = []
		self.conditions, self.values = self.get_conditions(self.filters)
		# frappe.errprint(f'self.conditions, self.values is ==>{self.conditions, self.values}')

		self.data = self.get_data_from_payment_entry(self.conditions,self.values)

		return self.data


	def get_data_from_payment_entry(self,conditions = '' ,values = ''):
		query_test_p = """
		select p.name as `Payment`,p.reference_no as `Cheques NO`,p.party as `Party`,p.party_type as `Party Type`,p.cheque_status as `Cheque Status`, p.paid_amount as `Amount`,p.posting_date as `Transaction Date`,p.reference_date as `Reference Date`,p.drawn_bank as `Bank`,p.drawn_bank_account as `Bank Account` 
		from `tabPayment Entry` as p , `tabCheque` as cq
		WHERE {conditions} AND p.cheque <> '' AND p.cheque = cq.name
		""".format(conditions=conditions)
		data_dict_p = frappe.db.sql(query_test_p,values=values,as_dict=1)
		# frappe.errprint(data_dict_p)
		return data_dict_p

	def get_conditions(self,filters):
		conditions = "1=1 "
		values = dict()

		if filters.get("party_type"):
			conditions += " AND p.party_type =  %(party_type)s "
			values["party_type"] = filters.get("party_type")
			if filters.get('party'):
				conditions += " AND p.party=%(party)s"
				values['party'] = filters.get('party')


		if filters.get("payment_type"):
			conditions += " AND p.payment_type =  %(payment_type)s "
			values["payment_type"] = filters.get("payment_type")

		if filters.get("current_state"):
			if filters.get("current_state") == 'Rejected' or filters.get("current_state") == "Rejected in Bank":
				conditions += " AND p.cheque_status =  %(current_state)s " #AND p.docstatus = '2'
			else:
				conditions += " AND p.cheque_status =  %(current_state)s AND p.docstatus = '1' "
			values["current_state"] = filters.get("current_state")


		

		

		if filters.get("from_date"):
			if filters.get("from_date") and filters.get("to_date"):
				conditions += " AND CAST(p.posting_date AS DATE) >= %(from_date)s  AND CAST(p.posting_date AS DATE) <= %(to_date)s"
				values["from_date"] = filters.get("from_date")
				values["to_date"] = filters.get("to_date")

			elif filters.get("from_date"):
				conditions += " AND CAST(p.posting_date AS DATE) =  %(from_date)s "
				values["from_date"] = filters.get("from_date")

		return conditions, values