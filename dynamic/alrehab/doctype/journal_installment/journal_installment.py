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

#set DEBUG to 0 for production 
DEBUG  =0 
class Journalinstallment(Document):
	def validate(self) :
			if DEBUG == 1 :
				self.create_installment_entry()
	def on_submit(self):
		#self.cerate_contract()
		self.create_installment_entry()
		
	def on_cancel(self) :
		entry_list = frappe.get_list("installment Entry" , {"reference_doc" :"Journal installment" ,
						     				"document" :self.name} )
		print(entry_list)
		for entry in entry_list :
			frappe.db.set_value ( "installment Entry" , entry.get("name")
		       			,'status' ,'Canceled')
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
	
	def initiate_installment_entry(self , customer):
		entry = []
		"""
		in this function first check auto create and repeated  method

		repeated methods  :
		 yearly create one entry from document date 
		 monthly create 12 entry  
		 three months  4 entry
		 six months 2 entry  
		
		"""
		monthly_methods = {
			"One Month" : 12 ,
			"Three Months" : 4 , 
			"six Months" : 2 , 
			"Yearly" :1
		}
		penalty_repetition =1
		# check installment Entry Type to validate has penalty or not 
		has_penalty =  frappe.get_value("installment Entry Type" , self.type , "delay_penalty")
		if has_penalty :
			print("Has Has penaty !!!!!! ")
			#create entry depend on type monthly_method
			template_link =  frappe.get_value("installment Entry Type" , 
									 self.type , "financial_penalty_template")
			#penalty_repetition 
			penalty_template =  frappe.get_doc("Financial penalty template" , 
												       	template_link)
			
			if penalty_template.auto_create == 1 :
				print("Has Has auto_create  !!!!!! ")
				#check method 
				#get repetition count 
				penalty_repetition  = monthly_methods[penalty_template.monthly_method] or None
		months_add = 0	

		# if type is auto_cal (auto calculation)
		installment_type = frappe.get_value("installment Entry Type" , self.type , "auto_cal")

		if installment_type :
			year = frappe.get_doc("Commercial year" ,self.year)
			for due in year.dates :
				installment_entry = frappe.new_doc("installment Entry")
				installment_entry.item = frappe.get_value("installment Entry Type" , self.type , "item")
				installment_entry.type = self.type
				installment_entry.installment_value = self.value
				installment_entry.total_value = self.value
				installment_entry.due_date = due.due_date
				installment_entry.status = "Under collection"
				installment_entry.customer      = customer
				installment_entry.reference_doc = "Journal installment"
				installment_entry.document      = self.name
				installment_entry.insert()
			return 1
		for i in range(1 ,(int(penalty_repetition) +1 )):
			due_date =  self.date
			value = self.value
			
			
				#frappe.throw(str(due_date))
			if months_add  :
				#update due_date 
				print(months_add)
				due_date = frappe.utils.add_months(due_date, months_add)

			installment_entry = frappe.new_doc("installment Entry")
			installment_entry.item = frappe.get_value("installment Entry Type" , self.type , "item")
			installment_entry.type = self.type
			installment_entry.installment_value = value
			installment_entry.total_value = value
			installment_entry.due_date = due_date
			installment_entry.status = "Under collection"
			installment_entry.customer      = customer
			installment_entry.reference_doc = "Journal installment"
			installment_entry.document      = self.name
			installment_entry.insert()
			if penalty_repetition > 1 :
				#calculate value
				#calculate date
				#months to add
				if penalty_repetition ==12  :
					months_add += 1
				if penalty_repetition ==2  :
					months_add += 6 
				if penalty_repetition ==4  :
					months_add += 3
			
		return 1

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
				entries = self.initiate_installment_entry(customer)
				# installment_entry.customer = customer
				# installment_entry.insert()
				# self.get_link(installment_entry)
				frappe.msgprint(_(" Entries Created "))

	def create_customer(self):
		entries = self.initiate_installment_entry(self.customer)
		# installment_entry = self.initiate_installment_entry()
		# installment_entry.customer = self.customer
		# installment_entry.insert()
		# self.get_link(installment_entry)
		frappe.msgprint(_(" Entries Created "))
	def get_link(self ,installment_entry):
		lnk = get_link_to_form(installment_entry.doctype, installment_entry.name)
		frappe.msgprint(_("{} {} was Created").format(
			installment_entry.doctype, lnk))
		return lnk
			 
		


	