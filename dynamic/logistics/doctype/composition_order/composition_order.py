# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import  get_link_to_form 
DOMAINS = frappe.get_active_domains()


class CompositionOrder(Document):
	@frappe.whitelist()
	def get_items(self):
		sales_order = frappe.get_doc("Sales Order" , self.sales_order)
		return sales_order.items
	
	@frappe.whitelist()
	def update_status(self):
		frappe.db.sql(f""" 
				UPDATE 
					`tabComposition Request` CO
				SET 
					CO.status = '{self.status}' 
				WHERE 
					CO.composition_order = '{self.name}' 
					AND
					CO.docstatus = 1
				""")
		
	@frappe.whitelist()
	def set_address_and_numbers(self):
		sql = f'''
			SELECT 
			 	CP.phone , C.address 
			FROM 
			  	`tabContact Phone` CP
			INNER JOIN 
				`tabContact` C
			ON 
				C.name = CP.parent
			INNER JOIN 
				`tabDynamic Link` DL
			ON 
				C.name = DL.parent
			WHERE 
				link_name = '{self.customer}'
			limit 3
			'''
		data = frappe.db.sql(sql , as_dict = 1)
		self.address = ''
		self.phone_number_1 = ''
		self.phone_number_2 = ''
		self.phone_number_3 = ''

		if data :
			if len(data) == 1:
				self.address = data[0]['address']
				self.phone_number_1 = data[0]['phone']
			if len(data) == 2:
				self.address = data[0]['address']
				self.phone_number_1 = data[0]['phone']
				self.phone_number_2 = data[1]["phone"]
			if len(data) == 3:
				self.address = data[0]['address']
				self.phone_number_1 = data[0]['phone']
				self.phone_number_2 = data[1]["phone"]
				self.phone_number_3 = data[2]["phone"]

	def on_submit(self):
		if 'Logistics' in DOMAINS :
			self.create_composition()

	def create_composition(self):
		composition = frappe.new_doc("Composition")
		composition.date = self.date 
		composition.sales_order = self.sales_order
		composition.status = self.status
		composition.customer = self.customer
		for item in self.items :
			composition.append("items" , {"item_code" :item.item_code ,"qty" :item.qty ,
								"delivery_date" :item.delivery_date ,"image" :item.image,
								"stock_uom" :item.stock_uom, "picked_qty" :item.picked_qty,
								"price_list_rate" :item.price_list_rate, "stock_qty" :item.stock_qty,
								"base_price_list_rate" :item.base_price_list_rate, 
								"rate" :item.rate ,"amount" :item.amount ,"base_rate" :item.base_rate , 
								"base_amount" :item.base_amount ,"is_free_item" :item.is_free_item ,
								"grant_commission" :item.grant_commission ,"net_rate" :item.net_rate ,
								"net_amount" :item.net_amount ,"base_net_rate" :item.base_net_rate ,
								"base_net_amount" :item.base_net_amount , "billed_amt" :item.billed_amt , 
								"valuation_rate" :item.valuation_rate ,  "gross_profit" :item.gross_profit , 
								"delivered_by_supplier" : item.delivered_by_supplier , "supplier" : item.supplier , 
								"weight_per_unit" : item.weight_per_unit , "total_weight" : item.total_weight ,
								"warehouse" : item.warehouse ,  "against_blanket_order" : item.against_blanket_order ,
								"projected_qty" : item.projected_qty ,  "actual_qty" : item.actual_qty ,
								"ordered_qty" : item.ordered_qty ,"work_order_qty" : item.work_order_qty ,
								"delivered_qty" : item.delivered_qty ,"produced_qty" : item.produced_qty ,
								"ensure_delivery_based_on_produced_serial_no" :item.ensure_delivery_based_on_produced_serial_no ,
								"item_name" :item.item_name , "description" :item.description ,
								"page_break" : item.page_break,
								"uom" :item.uom , "conversion_factor" : item.conversion_factor})
		composition.address = self.address
		composition.phone_number_1 = self.phone_number_1
		composition.phone_number_2 = self.phone_number_2
		composition.phone_number_3 = self.phone_number_3
		composition.link_location = self.link_location
		composition.engineers = self.engineers
		composition.customer_comment = self.customer_comment
		composition.location_is_ready = self.location_is_ready
		composition.save()
		self.composition = composition.name
		self.submit()

		lnk = get_link_to_form(composition.doctype, composition.name)
		frappe.msgprint(_("{} {} was Created").format(
		composition.doctype, lnk))
