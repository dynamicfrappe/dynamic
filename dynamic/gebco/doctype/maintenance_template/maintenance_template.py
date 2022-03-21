# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceTemplate(Document):
	def validate(self):
		self.validate_car_numbers()
	def validate_car_numbers(self):
		un_existing_list = []
		if self.maintenance_contract:
			contract = frappe.get_doc("Maintenance Contract",self.maintenance_contract)
			for pnumber in self.cars_plate_numbers:
				exist=False
				for p_number in contract.cars_plate_numbers:
					if p_number.plate_number == pnumber.plate_number:
						exist = True
				if not exist:
					un_existing_list.append(str(pnumber.plate_number))
		if len(un_existing_list) > 0:
			error_str = "".join(un_existing_list)
			frappe.throw(f"This Plate Number doesnt exist in contract {error_str}")

				
