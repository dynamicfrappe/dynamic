# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _ ,throw
from frappe import utils 
class MaintenancedepositCalculation(Document):
	def validate (self) : 
		if not self.unit_area :
			throw(_(f"Unit {self.unit} Has no area setting Please set unit area "))
		#self.Maintenance deposit
		if not self.items  :
			#add installment 24.75  
			#get un paid instalment 
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
						row.amount = item.installment_value 
						row.penalety = calculate_penalty_amount(self.unit_area ,item.due_date)
						row.total = float(item.installment_value  or 0 ) + float(row.penalety or 0)
						row.payment = row.total
						# calculate_penalty_amount(self.unit_area ,item.due_date)





def calculate_penalty_amount(unit_area , due_date):
	# days / years / months values 

	today = utils.get_datetime( utils.today())
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
	penalty_value = (float(monthly_value) * float(months_count) ) * float(unit_area)
	return penalty_value