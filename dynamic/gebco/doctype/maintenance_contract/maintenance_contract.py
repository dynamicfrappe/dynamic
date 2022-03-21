# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceContract(Document):
	pass

@frappe.whitelist()
def renew_contract(source_name, target_doc=None):
	doc = frappe.get_doc("Maintenance Contract", source_name)
	new_contract = frappe.new_doc("Maintenance Contract")
	new_contract.from_date  = doc.from_date
	new_contract.visits		= doc.visits
	new_contract.to_date 	= doc.to_date
	new_contract.number_of_visits = doc.number_of_visits
	new_contract.customer   	  = doc.customer
	new_contract.customer_name 	  = doc.customer_name
	new_contract.contract_value   = doc.contract_value
	new_contract.guarantee 		  = doc.guarantee
	new_contract.number_of_cars   = doc.number_of_cars
	for pl in doc.cars_plate_numbers:
		new_contract.append('cars_plate_numbers',{
			"plate_number":pl.plate_number
		})
	#new_contract.save()
	return new_contract



