# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class InstallationOrder(Document):
	def validate(self):
		self.set_totals()
		self.validate_qty()
		self.validate_schedule()

	def validate_qty(self):
		if self.installation_request:
			total_requested_qty = frappe.db.sql(f"""
			select SUM(total_cars) as total_cars  from `tabInstallation Order`
			where docstatus = 1 and name <> '{self.name}' and installation_request = '{self.installation_request}'
				""", as_dict=1)
			if total_requested_qty:
				total_requested_qty = total_requested_qty[0].total_cars or 0
			else :
				total_requested_qty = 0
			if (self.total_requested_cars-total_requested_qty) < self.total_cars:
				frappe.throw(_("""Request {} has {}/{} car is Already Requested""").format(
					self.installation_request,total_requested_qty,self.total_requested_cars
				))

		self.pending_cars = self.total_cars - self.completed_cars

	def validate_schedule(self):
		pass

	def on_submit(self):
		if self.installation_request:
			self.update_installation_request()
	
	def on_cancel(self):
		if self.installation_request:
			self.update_installation_request(cancel=1)
	
	def update_installation_request(self,cancel=0):
		installation_request = frappe.get_doc("Installation Request",self.installation_request)
		factor = -1 if cancel else 1
		installation_request.ordered_cars += factor * self.total_cars
		installation_request.validate()
		installation_request.save()
	
	@frappe.whitelist()
	def get_team_parties(self):
		if self.team :
			team = frappe.get_doc("Installation Team" , self.team )
			self.set("installation_team_detail",[])
			for emp in team.employees :
				self.append("installation_team_detail",{
					"employee":emp.employee,
					"employee_name":emp.employee_name
				})

		
	@frappe.whitelist()
	def set_totals(self):
		self.total_cars = sum([(x.cars or 0)
								for x in getattr(self, "items", [])])


@frappe.whitelist()
def make_installation(source_name):
    source = frappe.get_doc("Installation", source_name)
    if source.pending_cars <= 0:
        frappe.throw(_("there is no pending cars"))

    installation = frappe.new_doc("Installation")
    installation.installation_request = source.name
    installation.sales_order = source.sales_order

    installation.customer = source.customer
    installation.customer_name = source.customer_name
    installation.customer_phone_number = source.customer_phone_number

    installation.delegate = source.delegate
    installation.delegate_name = source.delegate_name
    installation.delegate_phone_number = source.delegate_phone_number

    installation.total_requested_cars = source.total_cars
    installation.total_cars = source.pending_cars
    installation.notes = source.notes
    return installation
