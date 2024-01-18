# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data


def get_data():
	conservation_requestes = frappe.get_all("Conservation Request" ,
								filters = {"docstatus" : 1} , fields = {"name"}) 
	return conservation_requestes

def get_columns():
	return [
		{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": _("Conservation Request"),
			"options":"Conservation Request",
			"width": 170
		},
	]

