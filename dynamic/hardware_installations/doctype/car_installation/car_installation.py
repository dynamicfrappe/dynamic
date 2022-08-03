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
		installation_order.ordered_cars += factor * self.total_cars
		installation_order.validate()
		installation_order.save()
		if installation_order.installation_request :
			update_installation_request_qty(installation_order.installation_request)

	@frappe.whitelist()
	def get_car_data(self):
		if self.car:
			car_doc = frappe.get_doc("Car",self.car)
			# car_model = frappe
			self.db_set("car_type",car_doc.get('device_type'))
			self.db_set("car_model",car_doc.get('serial_no'))

