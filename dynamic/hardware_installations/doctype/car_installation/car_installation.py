# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CarInstallation(Document):
	
	@frappe.whitelist()
	def get_car_data(self):
		if self.car:
			car_doc = frappe.get_doc("Car",self.car)
			# car_model = frappe
			self.db_set("car_type",car_doc.get('car_type'))
			self.db_set("car_model",car_doc.get('car_model'))
			self.db_set("car_brand",car_doc.get('car_brand'))
			if car_doc.device_type == "GEBCO":
				serial_doc = frappe.get_doc("Serial No",car_doc.serial_no)
				self.db_set("device_name",serial_doc.get('item_code'))
				self.db_set("serial_no",serial_doc.get('serial2'))
				self.db_set("imei_no",serial_doc.get('name'))

	@frappe.whitelist()
	def get_cst_delgate(self):
		if self.installation_order:
			install_req = frappe.get_doc("Installation Order",self.installation_order)
			self.db_set("customer",install_req.get('customer'))
			self.db_set("customer_name",install_req.get('customer_name'))
			self.db_set("customer_phone_number",install_req.get('customer_phone_number'))
			self.db_set("delegate",install_req.get('delegate'))
			self.db_set("delegate_name",install_req.get('delegate_name'))
			self.db_set("delegate_phone_number",install_req.get('delegate_phone_number'))

