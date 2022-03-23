# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaintenanceContract(Document):
	def validate(self):
		self.validate_car_numbers()

	def validate_car_numbers(self):
		car_numbers = self.number_of_cars
		count = 0
		for car in self.cars_plate_numbers:
			if car.status == "Active":
				count +=1
		if count > car_numbers :
			frappe.throw(f"You Only Have {car_numbers} in contract")
	@frappe.whitelist()
	def get_customers_cars(self,customer):
		sql = f"""select name from tabCar where customer='{customer}'"""
		cars = frappe.db.sql(sql,as_dict=1)
		self.cars_plate_numbers = {}
		# self.save()
		for c in cars:
			self.append('cars_plate_numbers',{
				'plate_number':c.name,
				'status':'Active'
			})
		return True
		#self.save()
		#self.reload_doc()
		#print("carss  =>",cars)
		#self.save()
	@frappe.whitelist()
	def update_doc_status(self,*args,**kwargs):
		self.status="Completed"
		self.save()

@frappe.whitelist()
def renew_contract(source_name, target_doc=None):
	doc = frappe.get_doc("Maintenance Contract", source_name)
	new_contract = frappe.new_doc("Maintenance Contract")
	new_contract.from_date  = doc.from_date
	new_contract.visits		= doc.visits
	new_contract.to_date 	= doc.to_date
	new_contract.number_of_visits = doc.number_of_visits
	new_contract.customer   	  = doc.customer
	new_contract.customer_name 	  = doc.customer_name
	new_contract.contract_value   = doc.contract_value
	new_contract.guarantee 		  = doc.guarantee
	new_contract.number_of_cars   = doc.number_of_cars
	for pl in doc.cars_plate_numbers:
		new_contract.append('cars_plate_numbers',{
			"plate_number":pl.plate_number
		})
	#new_contract.save()
	return new_contract


# @frappe.whitelist()
# def get_customers_cars(customer):
# 	sql = f"""select name from tabCar where customer='{customer}'"""
# 	print("sqllllll",sql)
# 	cars = frappe.db.sql(sql,as_dict=1)
# 	for c in cars:
# 		self.append('cars_plate_numbers',{
# 			'plate_number':c.name
# 		})
# 	#print("carss  =>",cars)
# 	self.save()


