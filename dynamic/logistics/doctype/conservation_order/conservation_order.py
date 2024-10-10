# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
from frappe import _


class Conservationorder(Document):
	@frappe.whitelist()
	def get_warranties(self , serial_number):
		item = frappe.db.get_value('Serial No', serial_number ,["item_code", "warranty_expiry_date"], as_dict=1)

		item_code = frappe.get_value(
               "Item", item.get("item_code"), ["item_name", "description" , "stock_uom"], as_dict=1)
		res = {
				'item_code':item_code.get("item_code"),
				'item_name':item_code.get("item_name"),
				'description':item_code.get("description"),
				'warranty_expiry_date':item.get("warranty_expiry_date"),
				'item_code':item.get("item_code"),
				'uom': item_code.get("stock_uom")
			}
		return res

	def validate_enginners(self):
		if self.engineering_name :
			for engineer in self.engineering_name :
				if engineer.from1 >= engineer.to :
					frappe.throw(_(f"From must be before to of row {engineer.idx} in enginnering table"))
				else :
					sql = f'''
						select 
							* 
						from 
							`tabEngineering Name` e
						where
							e.parenttype = "Conservation order"
								and 
							e.employee = '{engineer.employee}' 
								and
							('{engineer.from1}' between e.from1 and e.to 
								or 
							'{engineer.to}' between e.from1 and e.to )
						'''
					if engineer.name  :
						sql = sql +f"and e.name  != '{engineer.name}'"
					data = frappe.db.sql(sql, as_dict = 1)
					if data :
						frappe.throw(_(f"This range of row assigned to this employee in {data[0]['from1']} - {data[0]['to']} "))
	
	def before_validate(self):
		self.validate_enginners()

	def validate(self):
		self.calculate_total_cost()

	def on_submit(self):
		self.create_conservation()
		self.create_event()

	def calculate_total_cost(self):
		sum = 0
		if self.items:
			for item in self.items :
				if item.rate:
					sum += item.rate
		if self.service_items:
			for item in self.service_items:
				if item.rate:
					sum += item.rate
		if self.transfer_cost :
			sum += self.transfer_cost
		self.total_cost = sum

	def create_conservation(self):
		conservation = frappe.new_doc("Conservation")
		conservation.customer = self.customer
		conservation.customer_name = self.customer_name
		conservation.customer_primary_contact = self.customer_primary_contact
		conservation.customer_primary_address = self.customer_primary_address
		conservation.support = self.support
		conservation.support_reason = self.support_reason
		conservation.not_support = self.not_support
		conservation.not_support_reason = self.not_support_reason
		conservation.location = self.location
		conservation.type_for_request = self.type_for_request
		conservation.name_of_maintenance = self.name_of_maintenance
		conservation.number = self.number
		conservation.warranties = self.warranties
		conservation.machines = self.machines
		conservation.customer_comment = self.customer_comment
		conservation.description_of_maintenance_manager = self.description_of_maintenance_manager
		conservation.maintenance_type = self.maintenance_type
		if self.type_of_maintenance :
			conservation.type_of_maintenance = self.type_of_maintenance
		if self.items :
			conservation.items = self.items
		if self.service_items :
			conservation.service_items = self.service_items
		if self.transfer_cost :
			conservation.transfer_cost = self.transfer_cost
		if self.total_cost :
			conservation.total_cost = self.total_cost
		conservation.engineering_name = self.engineering_name
		conservation.insert()

		lnk = get_link_to_form(conservation.doctype, conservation.name)
		frappe.msgprint(_("{} {} was Created").format(
		conservation.doctype, lnk))
		self.db_set("conservation",conservation.name)

	def create_event(self):
		if self.engineering_name :
			for entry in self.engineering_name :
				event = frappe.new_doc("Event")
				event.subject = self.name
				event.starts_on = entry.from1
				event.ends_on = entry.to
				event.append("event_participants" , 
				 			{"reference_doctype" : "Employee" , "reference_docname" : entry.employee})
				event.insert()


@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.
	frappe
	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	filters = json.loads(filters)
	conditions = get_event_conditions("Conservation order", filters)

	data = frappe.db.sql("""
		select
			`tabConservation order`.name as name,
			`tabEngineering Name`.from1 as start,
			`tabEngineering Name`.to as end
		from
			`tabConservation order` 
		inner join 
			`tabEngineering Name`
			on
		    `tabConservation order`.name = `tabEngineering Name`.parent
			where
			(`tabEngineering Name`.from1 between %(start)s and %(end)s)
			{conditions}
		""".format(conditions=conditions),
		{"start": start, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)
	return data
