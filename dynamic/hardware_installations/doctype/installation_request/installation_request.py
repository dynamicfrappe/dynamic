# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

from gettext import install
import frappe
from frappe import _
from frappe.model.document import Document


class InstallationRequest(Document):
	def validate(self):
		self.validate_qty()

	def validate_qty(self):
		self.pending_cars = self.total_cars - self.completed_cars
		self.not_ordered_cars = self.total_cars - self.ordered_cars
		# frappe.throw(str(self.not_ordered_cars))


@frappe.whitelist()
def make_installation_order(source_name):
	source = frappe.get_doc("Installation Request" , source_name)
	if source.not_ordered_cars <= 0 :
		frappe.throw(_("there is no pending cars"))
	
	installation_order = frappe.new_doc("Installation Order")
	installation_order.installation_request = source.name
	installation_order.sales_order = source.sales_order
	
	installation_order.customer = source.customer
	installation_order.customer_name = source.customer_name
	installation_order.customer_phone_number = source.customer_phone_number
	
	installation_order.delegate = source.delegate
	installation_order.delegate_name = source.delegate_name
	installation_order.delegate_phone_number = source.delegate_phone_number


	
	installation_order.total_requested_cars = source.total_cars
	installation_order.total_cars = source.not_ordered_cars
	installation_order.notes = source.notes
	return installation_order
	