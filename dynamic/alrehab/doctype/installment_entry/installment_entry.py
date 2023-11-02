# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.data import  get_link_to_form 
from frappe.model.document import Document
from datetime import date


Domains=frappe.get_active_domains()
class installmentEntry(Document):
	def on_change(self) :
		if "Rehab"  in Domains :
			self.create_journal_entry()
			
	# def validate(self) :
	# 	self.create_journal_entry()

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
		if not doc.ignore_delay_penalty:
			area_c = frappe.db.get_value('Customer', doc.customer , 'unit_area')
			pay_template = frappe.get_doc("installment Entry Type" , doc.type)
			penality_template = False
			if pay_template.financial_penalty_template :
				penality_template  = frappe.get_doc("Financial penalty template" , pay_template.financial_penalty_template)
			if penality_template :
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
									if i.filed=="Item Unit Value" :
										eq_string = eq_string + f"{area_c}"
									if i.filed=="Days" :
										#caculate days 
										c_days= 1 
										date_diff = date.today() - doc.due_date 
										eq_string = eq_string + f"{date_diff.days}" 	
						else :
							eq_string = eq_string +  a

			equation_value = eval(eq_string) or 0
			if equation_value:
				self.db_set('delay_penalty',equation_value)
				out_stand = (float(self.total_value or 0) + float(equation_value)) - float(self.total_payed or 0)
				self.db_set('outstanding_value',out_stand)
				

