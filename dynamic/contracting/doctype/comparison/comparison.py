# Copyright (c) 2021, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json
class Comparison(Document):
	@frappe.whitelist()
	def get_items(self, for_raw_material_request=0):
		items = []
		for i in self.item:
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
	print("from ifffffffffffff",items)
	print("comparison",comparison)
	for item in items:
		doc = frappe.new_doc("Comparison Item Card")
		doc.item_code  = item.get("item_code")
		doc.comparison = comparison
		doc.tender	   = tender
		doc.save()
	return True