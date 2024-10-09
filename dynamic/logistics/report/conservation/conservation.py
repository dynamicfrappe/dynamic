# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data


def get_data():
	sql = f'''
			SELECT 
				C.customer , C.customer_name , C.type_for_request , C.support ,
				C.customer_comment , C.maintenance_type , C.description_of_maintenance_manager ,
				C.transfer_cost , C.total_cost ,
				W.item_code , W.description , W.warranty , W.serial_number ,
				M.machine_code , MA.maintenance ,
				P.item_code AS item_planed , S.item , S.rate ,
				E.employee , E.from1 , E.to 
			FROM
				`tabConservation` C
			INNER JOIN 
				`tabMaintenance Warranty` W
				ON
				C.name = W.parent 
			INNER JOIN 
				`tabCustomer Machine` M
				ON
				C.name = M.parent 
			INNER JOIN 
				`tabMaintenance Item` MA
				ON
				C.name = MA.parent 
			INNER JOIN 
				`tabPlaned Item` P
				ON
				C.name = P.parent 
			INNER JOIN 
				`tabService Item` S
				ON
				C.name = S.parent 
			INNER JOIN 
				`tabEngineering Name` E
				ON
				C.name = E.parent 
			'''  
	conservation_orders= frappe.db.sql(sql , as_dict =1 )
	# frappe.throw()
	return ""

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