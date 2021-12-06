# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json
class Comparison(Document):
	def validate(self):
		self.calc_taxes_and_totals()
	def calc_taxes_and_totals(self):
		total_items = 0
		total_tax  = 0
		#### calc total items
		for item in self.item:
			total_items += float(item.qty or 0) * float(item.price or 0)
		for t in self.taxes:
			t.tax_amount = float(total_items or 0) * (t.rate /100)
			total_tax += float(t.tax_amount or 0)
			t.total =  total_items +total_tax
		grand_total = total_items + total_tax
		ins_value          = grand_total * (self.insurance_value_rate / 100)
		delivery_ins_value = grand_total * (self.delevery_insurance_value_rate_ / 100)
		self.total_price = total_items
		self.tax_total   = total_tax
		self.delivery_insurance_value = delivery_ins_value
		self.insurance_value = ins_value
		self.total_insurance = ins_value + delivery_ins_value
		self.grand_total = grand_total
		self.total = grand_total

	@frappe.whitelist()
	def get_items(self, for_raw_material_request=0):
		items = []
		for i in self.item:
			if not i.comparison_item_card:
				items.append(dict(
					name=i.name,
					item_code=i.clearance_item,
					qty=i.qty,
					price=i.price,
					total=i.total_price
				))
		return items
@frappe.whitelist()
def get_item_price(item_code):
	try :
		if item_code:
			price_list = frappe.db.sql(f"""select * from `tabItem Price` where item_code='{item_code}' and selling=1""",as_dict=1)
			print("price_list",price_list)
			if len(price_list) > 0:
				return price_list[0].price_list_rate
			return 0
	except:
		pass

@frappe.whitelist()
def make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)

	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")
		target.update({'customer': source.customer})
		target.update({'is_contracting': 1})

	doclist = get_mapped_doc("Comparison", source_name, {
		"Comparison": {
			"doctype": "Sales Order",
			# "field_map": {
			# 	"customer": "customer",
			# },
		},
		"Comparison Item": {
			"doctype": "Sales Order Item",
			"field_map": {
				"name": "sales_order_item",
				"parent": "sales_order",
				"price":"rate",
				"clearance_item":"item_code"
			},
			"add_if_empty": True
		},
		"Purchase Taxes and Charges Clearances": {
			"doctype": "Sales Taxes and Charges",
			"field_map": {
				"name": "taxes",
				"parent": "sales_order"
			},
			"add_if_empty": True
		},
	}, target_doc,postprocess, ignore_permissions=ignore_permissions)

	return doclist
@frappe.whitelist()
def create_item_cart(items,comparison,tender=None):
	items = json.loads(items).get('items')
	# print("from ifffffffffffff",items)
	# print("comparison",comparison)
	name_list = []
	for item in items:
		doc = frappe.new_doc("Comparison Item Card")
		doc.item_comparison_number = item.get("idx")
		doc.qty = 1
		doc.item_code  = item.get("item_code")
		doc.comparison = comparison
		doc.tender	   = tender
		doc.flags.ignore_mandatory = 1
		doc.save()
		name_list.append({
			"item_cart":doc.name,
			"row_id" :item.get("idx")
		})
	if name_list:
		c_doc = frappe.get_doc("Comparison",comparison)
		for n in name_list:
			for item in c_doc.item:
				if n.get("row_id") == item.get("idx"):
					item.comparison_item_card = n.get("item_cart")
		c_doc.save()
	return True