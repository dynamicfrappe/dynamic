# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data


def get_data(filters):
	final_data = []
	conditions = " 1=1"

	if filters.get("sales_invoice") :
		conditions += f" and SI.name = '{filters.get('sales_invoice')}'"
	if filters.get("customer") :
		conditions += f" and SI.customer = '{filters.get('customer')}'"

	sql = f'''
		SELECT
			SII.item_code , SII.item_name , SII.qty , SI.creation , SII.brand ,
			SII.amount , SII.rate , SII.warehouse , SI.name , SI.selling_price_list ,
			SII.item_group
		FROM 
			`tabSales Invoice Item` SII
		INNER JOIN 
			`tabSales Invoice` SI
		ON 
			SI.name = SII.parent
		WHERE 
			{conditions} and SI.docstatus = 1
		ORDER BY 
				SI.name
		'''
	items = frappe.db.sql(sql , as_dict = 1)
	# frappe.throw(str(items))
	for item in items :
		dict = {}
		sql = f'''
			SELECT
				PII.rate as last_purchase , PI.posting_date as purchase_date
			FROM 
				`tabPurchase Invoice Item` PII
			INNER JOIN 
				`tabPurchase Invoice` PI
			ON 
				PI.name = PII.parent 
			WHERE 
				PII.item_code = '{item['item_code']}'

		'''
		purchase = frappe.db.sql(sql , as_dict = 1)
		if purchase :
			purchase_items = purchase[0]
	
		sql1 =f'''
			SELECT
				valuation_rate 
			FROM 
				`tabBin` 
			WHERE 
					item_code = '{item['item_code']}' 
				and
					warehouse = '{item['warehouse']}'
		'''
		valuation = frappe.db.sql(sql1 , as_dict = 1)
		if valuation :
			valuation_rate = valuation[0]
		
		sql2 = f'''
			SELECT
				SII.rate , SI.posting_date  , SI.name , SI.creation
			FROM 
				`tabSales Invoice Item` SII
			INNER JOIN 
				`tabSales Invoice` SI
			ON 
				SI.name = SII.parent
			WHERE 
				SII.item_code = '{item['item_code']}' 
				and SI.creation < '{item["creation"]}'
			ORDER BY 
				SII.parent 
		'''
		post_rate = frappe.db.sql(sql2 , as_dict = 1)

		dict["item_code"] = f'{item["item_code"]}'
		dict["selling_price_list"] = f'{item["selling_price_list"]}'
		dict["brand"] = f'{item["brand"]}'
		dict["item_group"] = f'{item["item_group"]}'


		dict["item_name"] = f'{item["item_name"]}'
		dict["qty"] = item["qty"]
		dict["sales"] = item["amount"]
		dict["cost"] = valuation_rate["valuation_rate"] * item["qty"]
		dict["purchases"] = item["qty"] * purchase_items["last_purchase"]
		dict["profit"] = dict["sales"] - dict["purchases"]
		if dict["purchases"] == 0 :
			dict["percentage"] = 0
		else :
			dict["percentage"] = dict["profit"] /dict["purchases"] * 100
		dict["item_price"] = item["rate"]
		dict["last_purchase"] = f'{purchase_items["last_purchase"]}' + ' - '  + f'{purchase_items["purchase_date"]}' 
		dict["unit_cost"] = valuation_rate["valuation_rate"]

		if post_rate :
			try:
				dict["rate_1"] = f'{post_rate[0]["rate"]}' 
			except (IndexError, KeyError):
				dict["rate_1"] = 0.0

			try:
				dict["rate_2"] = post_rate[1]["rate"]  
			except (IndexError, KeyError):
				dict["rate_2"] = 0.0 

			try:
				dict["rate_3"] = post_rate[2]["rate"] 
			except (IndexError, KeyError):
				dict["rate_3"] = 0.0
		# if post_rate :
		# 	try:
		# 		dict["rate_1"] = f'{post_rate[0]["rate"]}' + ' - ' + f'{post_rate[0]["posting_date"]}' 
		# 	except (IndexError, KeyError):
		# 		dict["rate_1"] = 0.0

		# 	try:
		# 		dict["rate_2"] = post_rate[1]["rate"] + ' - ' + f'{post_rate[0]["posting_date"]}' 
		# 	except (IndexError, KeyError):
		# 		dict["rate_2"] = 0.0 

		# 	try:
		# 		dict["rate_3"] = post_rate[2]["rate"] + ' - ' + f'{post_rate[0]["posting_date"]}' 
		# 	except (IndexError, KeyError):
		# 		dict["rate_3"] = 0.0
		final_data.append(dict)
	return final_data

def get_rate_and_date(post_rate, index):
    try:
        rate = f'{post_rate[index]["rate"]}'
        date = f'{post_rate[index]["posting_date"]}'
        return f'{rate} - {date}'
    except (IndexError, KeyError):
        return 0.0
			

def get_columns( num_rates=3 ):
	columns = [ 
				# { 
				# 	"label": _("Sale Invoice"), 
				# 	"fieldname": "sale_invoice", 
				# 	"fieldtype": "Link", 
				# 	"options": "Sale Invoice", 
				# 	"width": 100, 
				# }, 
				{ 
					"label": _("Item Code"), 
					"fieldname": "item_code", 
					"fieldtype": "Link", 
					"options": "Item", 
					"width": 100, 
				}, 
				{ 
					"label": _("Item Grouo"), 
					"fieldname": "item_group", 
					"fieldtype": "Link", 
					"options": "Item Group", 
					"width": 100, 
				}, 
				{ 
					"label": _("Item Name"), 
					"fieldname": "item_name", 
					"fieldtype": "Data", 
					"width": 100, 
				}, 
				{ 
					"label": _("Quantity"), 
					"fieldname": "qty", 
					"fieldtype": "Data", 
					"width": 100, 
				},
				{
					"label": _("Sales"),
					"fieldname": "sales",
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				}, 
				{ 
					"label": _("Price List"), 
					"fieldname": "selling_price_list", 
					"fieldtype": "Link", 
					"options": "Price List", 
					"width": 100, 
				}, 
				{ 
					"label": _("Brand"), 
					"fieldname": "brand", 
					"fieldtype": "Data", 
					"width": 100, 
				},
				{
					"label": _("Cost"),
					"fieldname": "cost",
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				},
				{
					"label": _("Purchases"),
					"fieldname": "purchases",
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				},
				{
					"label": _("Profit"),
					"fieldname": "profit",
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				},
				{
					"label": "Percentage",
					"fieldname": "percentage",
					"fieldtype": "Float",
					"width": 150,
          	    },
				{
					"label": _("Item Price"),
					"fieldname": "item_price",
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				},

				{ 
					"label": _("Last Purchase"), 
					"fieldname": "last_purchase", 
					"fieldtype": "Data", 
					"width": 100, 
				},
				{
					"label": _("Unit Cost"),
					"fieldname": "unit_cost",
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				},
	    ]
	for i in range(1, num_rates + 1): 
			columns.extend([ 
				{ 
					"label": _("Rate {}".format(i)), 
					"fieldname": "rate_{}".format(i), 
					"fieldtype": "Data", 
					"width": 200, 
				}, 
			])
							
	return columns


			
