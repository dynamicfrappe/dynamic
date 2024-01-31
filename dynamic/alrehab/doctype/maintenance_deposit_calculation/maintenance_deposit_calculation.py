# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _ ,throw
from frappe import utils 


from dynamic.alrehab.utils import get_mode_of_payment_account ,get_customer_default_account


class MaintenancedepositCalculation(Document):
	def validate (self) : 
		if not self.unit_area :
			throw(_(f"Unit {self.unit} Has no area setting Please set unit area "))
		#self.Maintenance deposit
		if not self.items  :
			#get un paid instalment 
			self.set_installment_items()		

		if self.type == "Maintenance deposit" :
			self.recalculate_penalty()
				
			self.calculate_payments()
		self.validate_payment_method_account()
		self.calculate_total_payment()
		if not self.posting_date :
			self.posting_date = utils.today()
		self.calculate_total()
	def on_submit(self):
		"""
		last validation 
		create journal entry 
		update installment entry 
		update Maintenance deposit line status 
		"""
		#self.validate_installment_unit()
		self.create_journal_entry()


	def on_cancel(self) :
		"""
		cancel all journal entry
		remove paid from installment entry 
		remove paid from Maintenance deposit line
		"""
		# cancel entry throw linked installment entry 
		for item in self.items :
			install_entry = frappe.get_doc("installment Entry" , item.installment_entry	 )
			install_entry.clear_ledger()
			install_entry.save()
			frappe.db.sql(f""" 
			UPDATE `tabMaintenance Deposit installments Items`  
			SET paid = 0 WHERE name ='{item.line}'

			""")
			frappe.db.commit()
	
	# VALIDATE METHOD 
	def set_installment_items(self) :
		if self.type == "Maintenance deposit" :
				
				self.set_installment_items_maintenance()

		if self.type == "Yearly Payment" :
			self.set_installment_items_yearly()



	# update start 

	def set_installment_items_yearly(self):

		"""Map data :
		Document -- Journal installment  (to get year variable )
		Type     -- installment Entry Type to check if it has late penalty or not and if it depend on year variable
				"""
		entry_list = frappe.get_list("installment Entry" ,
			                        fields = ["name" ,"installment_value" , "due_date" ,"document" ,"type"] ,
			        						filters = {"reference_doc" :"Journal installment" ,
						     				"customer" :self.unit ,"status": "Not Paid"} )
		
		for entry in entry_list :
			#set default value 
			value = float(entry.installment_value) 
			print(entry)
			#set penalty variable value 
			penalty_variable = 0
			#check type 
			# template = 
			installment_type = frappe.get_doc("installment Entry Type" , entry.type) 
			if installment_type.delay_penalty == 1 :
				#calculate penalty 
				# 1- get template   
				template = frappe.get_doc("Financial penalty template" ,installment_type.financial_penalty_template )
				if template.required_year_value ==1 :
					year = frappe.get_value("Journal installment" ,entry.document ,"year" )
					#calculate factor 
					penalty_variable  =  frappe.get_value("Commercial year" ,year ,"factor" )
			row = self.append("items" , {})
			row.installment_entry = entry.name
			row.due_date = entry.due_date 
			#row.line = item.name 
			row.amount = entry.installment_value
			allocated_info = calculate_penalty_amount(self.unit_area ,entry.due_date ,self.posting_date ,True ,penalty_variable )
			print("Allocated" , allocated_info)
			row.penalety = allocated_info[0]
			row.days_count = allocated_info[2]
			row.months_count = allocated_info[1]
			row.total =  float(entry.installment_value or 0 ) + float(row.penalety or 0)
			row.payment = row.total
	# end Update
	def set_installment_items_maintenance(self) :
		maintenance_deposit = frappe.db.sql(f""" SELECT name FROM `tabMaintenance deposit` 
		WHERE unit = '{self.unit}' and docstatus = 1""" ,as_dict =1)
		if not maintenance_deposit or len(maintenance_deposit) == 0 :
			throw(_(f"""  No Maintenance deposit For this unit {self.unit} """))
		for md in maintenance_deposit :
			link_doc =frappe.get_doc( "Maintenance deposit" ,  md.get("name"))
			for item in link_doc.maintenance_deposit_installments_items :
				if not item.paid :
					row = self.append("items" , {})
					row.installment_entry = item.reference_entry 
					row.maintenance_deposit = md.name 
					row.due_date = item.due_date
					row.line = item.name  
					row.amount = item.installment_value 
					allocated_info = calculate_penalty_amount(self.unit_area ,item.due_date)
					row.penalety = allocated_info[0]
					row.days_count = allocated_info[2]
					row.months_count = allocated_info[1]
					row.total = float(item.installment_value  or 0 ) + float(row.penalety or 0)
					row.payment = row.total
	def recalculate_penalty(self) :
		if self.type == "Maintenance deposit" :
			if self.posting_date and self.edit_posting_date == 1 :
				for item in self.items :
					allocated_info =calculate_penalty_amount(self.unit_area ,item.due_date ,self.posting_date)
					item.penalety =  allocated_info[0]
					item.total = float(item.amount  or 0 ) + float(item.penalety or 0)
					item.payment = item.total
	def calculate_total(self) :
		self.total=0 
		for i in self.items  :
			self.total += float(i.total)

	def calculate_total_payment(self) :
		#total section calculation
		self.total_amount = 0 
		self.total_penalty = 0
		for item in self.items :
			self.total_amount = float(item.amount or 0 )
			self.total_penalty = float(item.penalety ) or 0 
		self.grand_total = self.total_amount + self.total_penalty
	def calculate_payments(self) :
		self.total_payment = 0 
		for item in self.items :
			self.total_payment += item.payment
	def validate_payment_method_account(self) :
		if self.payment_method :
			payment_account = get_mode_of_payment_account(self.payment_method , self.company)
			if not payment_account :
				frappe.throw(f""" Please Set default company {self.company} account in mode of payment {self.payment_method}""")
	# SUBMIT METHOD 

	def validate_installment_unit(self) :
		"""
		validate unit
		validate is paid installment

		"""
		for item in self.items :
			if not item.installment_entry :
				frappe.throw(_(f"""Can Not Submit coz due date {item.due_date} installment dont belong to any Entry """))
			if self.unit != frappe.get_value("installment Entry" ,  item.installment_entry , 'customer') :
				frappe.throw(_(f""" Due Date {item.due_date} installment
				  entry is {frappe.get_value("installment Entry" ,  item.installment_entry , 'customer')}  and current unit is {self.unit}"""))
			if frappe.get_value("installment Entry" ,  item.installment_entry , 'is_paid') == 1 :
				frappe.throw(_(f""" Installment already paid before {item.due_date} """))


	def create_journal_entry(self) :
		''''
		each line has his payment entry 
		customer against income account from settings
		payment method account against customer account 

		1- create customer selling entry
		'''
      #get_customer default account 
		default_selling_account  = frappe.db.get_value("Company", self.company ,"default_receivable_account")
		default_customer_account = get_customer_default_account( self.unit, self.company) 
		if default_customer_account and default_customer_account != 0  :
			default_selling_account = default_customer_account
		if not default_selling_account :
			frappe.throw(f""" please set unit {self.unit}  default account or set company default receivable account""")
		

		#get default selling account 
		selling_account = frappe.db.get_single_value("Maintenance deposit Setting", "income_account")
		cost_center = frappe.db.get_single_value("Maintenance deposit Setting", "cost_centr")
		payed_account =get_mode_of_payment_account(self.payment_method ,self.company)
		
		if not selling_account :
				frappe.throw(_("""Please Set Income account in Maintenance deposit Setting """))
		if not cost_center :
				frappe.throw(_("""Please Set Cost Center in Maintenance deposit Setting """))
		for item in self.items :
			# get accounts 
			# Set selling account 
			installment_entry = frappe.get_doc("installment Entry" , item.installment_entry)
			entry = frappe.new_doc("Journal Entry")
			entry.voucher_type = "Journal Entry"
			entry.posting_date = self.posting_date  
			entry.installment_entry =installment_entry.name
			# debit account
			entry.append("accounts", {
			"account" : default_selling_account ,
			"party_type" : "Customer",
			"party" : self.unit ,
			"debit_in_account_currency": item.payment,
			"debit" :item.payment })
			#credit account
			entry.append("accounts" ,{
				"account" : selling_account ,
				"credit_in_account_currency" : item.payment , 
				"credit" : item.payment
			} )
			entry.save()
			
			installment_entry.append("claiming_entry" , {
				"type" :"Journal Entry" ,
				"document" : entry.name
			})
			installment_entry.income_account = selling_account
			installment_entry.is_clamed = 1
			installment_entry.save()
			# set installment claiming table 
			
			#set payment account
			payment_entry = frappe.new_doc("Journal Entry")
			payment_entry.voucher_type = "Journal Entry"
			payment_entry.posting_date = self.posting_date 
			payment_entry.installment_entry =installment_entry.name
			payment_entry.append("accounts" ,{
				"account" : default_selling_account ,
				"party_type" : "Customer",
				"party" : self.unit ,
				"credit_in_account_currency": item.payment,
				"credit" :item.payment
			})
			payment_entry.append("accounts" ,{
				"account" : payed_account ,
				"debit_in_account_currency" : item.payment , 
				"debit" : item.payment
			} )
			
			payment_entry.save()
			
			installment_entry.is_paid = 1
			installment_entry.total_payed = item.payment
			installment_entry.payment_day = self.posting_date
			installment_entry.delay_penalty = item.penalety
			installment_entry.total_value = item.total
			installment_entry.total_payed = item.amount
			installment_entry.status = "Paid"
			installment_entry.append("paid_entry" ,{
				"type" :"Journal Entry" ,
				"document" : payment_entry.name
			})
			installment_entry.save()
			payment_entry.submit()
			entry.submit()
			frappe.db.sql(f""" 
			UPDATE `tabMaintenance Deposit installments Items`  
			SET paid = 1 WHERE name ='{item.line}'

			""")
			frappe.db.commit()
def calculate_penalty_amount(unit_area , due_date ,posting_date =False ,daily =False ,variable =False):
	# days / years / months values 
	if not posting_date :
		today = utils.get_datetime( utils.today())
	if posting_date :
		today = utils.get_datetime(posting_date)
	duedate  =  utils.get_datetime(due_date)
   #get days count //
	difference_days = today-duedate # - due_date
	years_count = (float(difference_days.days) / 365 ) 
	months_count = years_count * 12 
	monthly_value =  frappe.db.get_single_value("Maintenance deposit Setting", "maintenance_deposit_monthly_percent")
	print(months_count)
	if float(monthly_value or 0 ) == 0 :
		frappe.throw("""Please Set  Maintenance deposit Monthly Percent in Maintenance deposit Settings""")
	# get penalty value
	if not daily :
		penalty_value = (float(monthly_value) * float(months_count) ) * float(unit_area)
		return (penalty_value ,months_count ,  difference_days.days)
	if daily :
		penalty_value =  (float(unit_area)  *4 )* float(difference_days.days or 0) * float(variable or 0)
		return (penalty_value ,months_count ,  difference_days.days)


