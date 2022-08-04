# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from dynamic.hardware_installations.doctype.installation_request.installation_request import update_installation_request_qty
import frappe
from frappe.model.document import Document

class CarInstallation(Document):
	def on_submit(self):
		if self.installation_order :
			self.update_installation_order()

	def on_cancell(self):
		if self.installation_order :
			self.update_installation_order(cancel=1)

	def update_installation_order (self,cancel=0):
		installation_order = frappe.get_doc(
			"Installation Order", self.installation_order)
		factor = -1 if cancel else 1
		installation_order.completed_cars += factor * 1
		installation_order.validate()
		installation_order.save()
		if installation_order.installation_request :
			update_installation_request_qty(installation_order.installation_request)

	@frappe.whitelist()
	def get_car_data(self):
		if self.car:
			car_doc = frappe.get_doc("Car",self.car)
			# car_model = frappe
			self.db_set("car_type",car_doc.get('car_type'))
			self.db_set("car_model",car_doc.get('car_model'))
			self.db_set("car_brand",car_doc.get('car_brand'))
			

	@frappe.whitelist()
	def get_cst_delgate(self):
		if self.installation_order:
			install_ord = frappe.get_doc("Installation Order",self.installation_order)
			self.db_set("customer",install_ord.get('customer'))
			self.db_set("customer_name",install_ord.get('customer_name'))
			self.db_set("customer_phone_number",install_ord.get('customer_phone_number'))
			self.db_set("delegate",install_ord.get('delegate'))
			self.db_set("delegate_name",install_ord.get('delegate_name'))
			self.db_set("delegate_phone_number",install_ord.get('delegate_phone_number'))
			if install_ord.installation_team_detail:
				self.team = install_ord.team
				self.installation_team_detail = []
				for row in install_ord.installation_team_detail:
					self.append('installation_team_detail', {
						'employee': row.employee,
						'employee_name': row.employee_name,
						})

	@frappe.whitelist()
	def get_serial_gps(self):
		if self.gps_type == "Internal":
				serial_doc = frappe.get_doc("Serial No",self.serial_number)
				# self.db_set("device_name",serial_doc.get('item_code'))
				self.db_set("gps_no",serial_doc.get('serial2'))
				self.db_set("gps_series",serial_doc.get('name'))