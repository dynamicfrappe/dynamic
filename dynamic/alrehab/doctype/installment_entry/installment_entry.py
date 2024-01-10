# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.data import  get_link_to_form 
from frappe.model.document import Document
from datetime import date
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
from frappe.utils.background_jobs import enqueue
from datetime import date
from dateutil import relativedelta
# from dateutil import relativedelta
Domains=frappe.get_active_domains()

class installmentEntry(Document):

	def validate(self):
		if  not self.get('__unsaved') and not self.claiming_entry:
			self.set_status()

	def after_insert(self):
		self.set_status()

	

	def create_journal_entry(self):
		if not self.is_clamed :
			journal_entry = frappe.new_doc("Journal Entry")
			journal_entry.posting_date = self.due_date
			company = frappe.defaults.get_user_default("Company")
			debitor_account = frappe.get_value("Company" , company , "default_receivable_account")
			journal_entry.installment_entry = self.name
			journal_entry.append("accounts" ,
						{"account" :debitor_account 
						, "party_type" : "Customer"
						,"party":self.customer 
						 , "debit_in_account_currency" :self.total_value
						  ,"credit_in_account_currency" : 0.00
						  ,"cost_center" : self.cost_center
						 }
						 )
			journal_entry.append("accounts" ,
						{"account" :self.income_account ,
						 "debit_in_account_currency" : 0.00,
						 "credit_in_account_currency" : self.total_value
						 ,"cost_center" : self.cost_center})
			journal_entry.insert()
			journal_entry.submit()

			lnk = get_link_to_form(journal_entry.doctype, journal_entry.name)
			frappe.msgprint(_("{} {} was Created").format(
				journal_entry.doctype, lnk))

	@frappe.whitelist()
	def caculate_installment_value(self):
		eq_string= ""
		doc = frappe.get_doc("installment Entry" , self.name)
		# print(f'\n\n\n self.name==>{self.name}')
		if not doc.ignore_delay_penalty:
			area_c = frappe.db.get_value('Customer', doc.customer , 'unit_area')
			pay_template = frappe.get_doc("installment Entry Type" , doc.type)
			penality_template = False
			if pay_template.financial_penalty_template  and pay_template.delay_penalty:
				penality_template  = frappe.get_doc("Financial penalty template" , pay_template.financial_penalty_template)
			if penality_template :
				# if penality_template.auto_create:
				equation_value = 1  * 1
				if penality_template.equation :
					variables = [i for i in penality_template.variables]
					# change string values with current value 
					for a in penality_template.equation :
						if a.isalnum() :
						#caculate a 
							for  i in variables :
								if i.variable == a :
									if i.filed == "Static Value":
										eq_string = eq_string +  i.value
										# print(f'\n\n\n eq_string++==>{eq_string}')
									if i.filed=="Item Unit Value" :
										eq_string = eq_string + f"{area_c}"
									if i.filed=="Days" :
										#caculate days 
										c_days= 1 
										date_diff = date.today() - doc.due_date 
										eq_string = eq_string + f"{date_diff.days}" 	
									if i.filed=="Months" :
										delta = relativedelta.relativedelta( date.today() ,doc.due_date )
										# print("mothes" ,delta.months)
										months = (float(delta.years or 0) *12 )+ float(delta.months) +  (float(delta.days) / 30)
										print("Mothes" , months)
										eq_string = eq_string + f"{months}"
						else :
							eq_string = eq_string +  a

					print( "\n\nn\eq --------------------" , eq_string,'\n\n\n')
					equation_value = eval(eq_string) or 0
				out_stand = 0
				if equation_value:
					self.db_set('delay_penalty',equation_value)
					if not self.outstanding_value:
						out_stand =  float(equation_value or 0 ) - float(self.total_payed or 0)
					if float(self.outstanding_value or 0):
						out_stand = float(equation_value)
					self.db_set('outstanding_value',out_stand)
				

	def set_status(self):
		if getdate(self.due_date) <= date.today() and self.status=='Under collection':
			self.status='Not Paid'
			self.create_journal_entry()

@frappe.whitelist()	
def get_installment_entry_to_update_status():
	data = f"""
	select name,CAST(`tabinstallment Entry`.due_date AS DATE) as due_date
	,`tabinstallment Entry`.due_date as d2 from `tabinstallment Entry` 
	where CAST(`tabinstallment Entry`.due_date AS DATE) <= CURDATE()
	AND `tabinstallment Entry`.status='Under collection'
	"""
	notify_role = ''
	data = frappe.db.sql(data,as_dict=1)
	if data :
		prepare_enque_data(notify_role,data,update_installment_entry_status)



def prepare_enque_data(role,data,method):
	kwargs={
		"data":data,
	}
	frappe.enqueue( 
	method=method,
	job_name="update_installment_entry_status",
	queue="default", 
	timeout=500, 
	is_async=False, # if this is True, method is run in worker
	now=True, # if this is True, method is run directly (not in a worker) 
	at_front=False, # put the job at the front of the queue
	**kwargs,
)



def update_installment_entry_status(**kwargs):
	for row in kwargs.get("data"):
		installment_entry = frappe.get_doc("installment Entry",row.name)
		installment_entry.status= 'Not Paid'
		installment_entry.create_journal_entry()
		installment_entry.save()
		frappe.db.commit()
		