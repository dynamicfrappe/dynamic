# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data


def get_data():
	conservation_sql = f'''
						SELECT 
							C.customer , C.type_for_request , C.from , C.to , C.maintenance_type , C.customer_comment ,
							M.item_code , M.serial_number , M.warranty , CM.machine_code , SI.item , SI.rate , SI.serial_number ,
							MI.maintenance , EN.employee , EN.from1 , EN.to
						FROM 
							`tabConservation` C
						INNER JOIN 
							`tabMaintenance Warranty` M ON C.name = M.parent
						INNER JOIN 
							`tabCustomer Machine` CM ON C.name = CM.parent
						INNER JOIN 
							`tabMaintenance Item` MI
						ON
							C.name = MI.parent
						INNER JOIN 
							`tabService Item` SI
						ON
							C.name = SI.parent
						INNER JOIN 
							`tabEngineering Name` EN
						ON
							C.name = EN.parent
						'''
	conservations = frappe.db.sql(conservation_sql , as_dict = 1) 
	# frappe.throw(str(conservation_sql))
	# return conservation_requestes

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

