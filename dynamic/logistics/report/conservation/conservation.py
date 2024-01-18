# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data


def get_data():
	conservation_orders= frappe.get_all("Conservation" ,
								filters = {"docstatus" : 1} , fields = {"name"}) 
	return conservation_orders

def get_columns():
	return [
		{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": _("Conservation"),
			"options":"Conservation",
			"width": 170
		},
	]