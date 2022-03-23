# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext import get_default_company

class MaintenanceTemplate(Document):
	def validate(self):
		self.validate_car_numbers()
	def validate_car_numbers(self):
		un_existing_list = []
		if self.maintenance_contract and len(self.maintenance_contract) > 0:
			contract = frappe.get_doc("Maintenance Contract",self.maintenance_contract)
			for pnumber in self.cars_plate_numbers:
				exist=False
				for p_number in contract.cars_plate_numbers:
					if p_number.plate_number == pnumber.plate_number:
						exist = True
				if not exist:
					un_existing_list.append(str(pnumber.plate_number))
		if len(un_existing_list) > 0:
			error_str = "".join(un_existing_list)
			frappe.throw(f"This Plate Number doesnt exist in contract {error_str}")
	
	@frappe.whitelist()
	def create_stock_entrys(self):
		try:
			doc = frappe.new_doc("Stock Entry")
			doc.stock_entry_type = "Material Issue"
			doc.company          = get_default_company()
			doc.maintenance_template = self.name
			#doc.save()
			for item in self.items:
				doc.append('items',{
					"s_warehouse": self.warehouse,
					"item_code":item.item,
					"item_name":item.item_name,
					"description":item.description,
					"qty":item.qty,
					"stock_uom":item.uom,
					"basic_rate":item.price
				})
			doc.save()
			doc.docstatus=1
			doc.save()
			self.stock_entry = doc.name
			frappe.msgprint("Stock Entry Created Successfully")
		except Exception as ex:
			frappe.msgprint(str(ex))

	@frappe.whitelist()
	def get_item_price(self,item_code):
		sql = f"""
			select price_list_rate FROM `tabItem Price` tip where item_code ='{item_code}' and price_list='Standard Selling' limit 1
		"""
		print("sql ========>",sql)
		result = frappe.db.sql(sql,as_dict=1)
		print("result ======>",result)
		if len(result) > 0:
			return result[0].price_list_rate
		else:
			return 0
	
@frappe.whitelist()
def create_delivery_note(source_name, target_doc=None):
	doc = frappe.get_doc("Maintenance Template" , source_name)
	delivery_note = frappe.new_doc("Delivery Note")
	delivery_note.company = get_default_company()
	delivery_note.customer = doc.customer
	delivery_note.maintenance_template = source_name
	for item in doc.items:
		delivery_note.append('items',
			{
				"item_code": item.item,
				"item_name":item.item_name,
				"description":item.item_name,
				"qty":item.qty,
				"stock_uom":item.uom,
				"uom":item.uom,
				"warehouse": doc.warehouse,
				"rate": item.price
			}
		)
	for item in doc.service_items:
		delivery_note.append('service_items',
			{
				"item_code": item.item,
				"item_name":item.item_name,
				"description":item.description,
				"qty":item.qty,
				"stock_uom":item.uom,
				"uom":item.uom,
				"warehouse": doc.warehouse,
				"rate": item.price
			}
		)
	return delivery_note


@frappe.whitelist()
def create_sales_invoice(source_name, target_doc=None):
	doc = frappe.get_doc("Maintenance Template" , source_name)
	company_doc = frappe.get_doc("Company",get_default_company())
	sales_invoice = frappe.new_doc("Sales Invoice")
	sales_invoice.company = get_default_company()
	sales_invoice.customer = doc.customer
	sales_invoice.maintenance_template = source_name
	for item in doc.items:
		sales_invoice.append('items',
			{
				"item_code": item.item,
				"item_name":item.item_name,
				"description":item.item_name,
				"qty":item.qty,
				"stock_uom":item.uom,
				"uom":item.uom,
				"warehouse": doc.warehouse,
				"rate": item.price,
				"income_account":company_doc.default_income_account,
				"cost_center":doc.cost_center
			}
		)
	for item in doc.service_items:
		sales_invoice.append('service_items',
			{
				"item_code": item.item,
				"item_name":item.item_name,
				"description":item.description,
				"qty":item.qty,
				"stock_uom":item.uom,
				"uom":item.uom,
				"warehouse": doc.warehouse,
				"rate": item.price
			}
		)
	return sales_invoice


				
