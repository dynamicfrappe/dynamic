# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 
from frappe.utils.data import  get_link_to_form 

from frappe.model.document import Document
from frappe.utils import (
	cint,
	cstr,
	flt,
	fmt_money,
	format_datetime,
	format_duration,
	format_time,
	format_timedelta,
	formatdate,
	getdate,
)

class Journalinstallment(Document):
	def validate(self):
		self.cerate_contract()
		self.create_installment_entry()

	def cerate_contract(self):
		if self.journal_type == "Contract" and self.contracted== 0:
			#create contract 
			contract = frappe.new_doc("Rehab Contract") 
			contract.unit = self.unit
			contract.installment_entry_type = self.type 
			contract.maintenance_deposit_value = self.maintenance_deposit_value 
			contract.maintenance_deposit_installments_count = self.maintenance_deposit_installments_count 
			item = frappe.get_value("installment Entry Type" , self.type , "item")
			for index in range(cint(self.maintenance_deposit_installments_count)):
				contract.append('maintenance_deposit_installments_items',{
					"item":item,
					"installment_value":flt(flt(self.maintenance_deposit_value) ),#/ cint(self.maintenance_deposit_installments_count) ),
					"due_date":getdate()
				})
			contract.save()
			self.contracted = 1
			self.contract = contract.name

	def create_installment_entry(self):
		if self.journal_type == "Customer Group":
			self.get_customers_with_customer_group()

		if self.journal_type == "All Customer" :
			self.get_cutomers_except_excluded()

		if self.journal_type == "One Customer" :
			self.create_customer()
	
	def initiate_installment_entry(self):
		installment_entry = frappe.new_doc("installment Entry")
		installment_entry.item = frappe.get_value("installment Entry Type" , self.type , "item")
		installment_entry.type = self.type
		installment_entry.installment_value = self.value
		installment_entry.total_value = self.value
		installment_entry.due_date = self.date
		installment_entry.status = "Under collection"
		return installment_entry

	def get_customers_with_customer_group(self):
		customers = frappe.get_all("Customer" , filters ={"customer_group" : self.customer_group}
							  , pluck="name")
		if len(customers) > 0 :
			for customer in customers :
				installment_entry = self.initiate_installment_entry()
				installment_entry.customer = customer
				installment_entry.insert()
				self.get_link(installment_entry)
	
	def get_cutomers_except_excluded(self):
		excluded_customers = []
		
		if self.exclude :
			for customer in self.customers :
				excluded_customers.append(customer.customer)
		customers = frappe.get_all("Customer" ,filters ={"customer_name" : ["not in" , excluded_customers]}
							, pluck="name")
		
		if len(customers) > 0 :
			for customer in customers :
				installment_entry = self.initiate_installment_entry()
				installment_entry.customer = customer
				installment_entry.insert()
				self.get_link(installment_entry)

	def create_customer(self):
		installment_entry = self.initiate_installment_entry()
		installment_entry.customer = self.customer
		installment_entry.insert()
		self.get_link(installment_entry)

	def get_link(self ,installment_entry):
		lnk = get_link_to_form(installment_entry.doctype, installment_entry.name)
		frappe.msgprint(_("{} {} was Created").format(
			installment_entry.doctype, lnk))
		return lnk
			 
		


	