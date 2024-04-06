# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	return columns, data

def get_data(filters):
	conditions = " 1=1"
	if filters.get("from_date") :
		conditions += f" and so.delivery_date >= '{filters.get('from_date')}'"
	if filters.get("to_date") :
		conditions += f" and so.delivery_date <= '{filters.get('to_date')}'"

	if filters.get("from_no") :
		conditions += f" and soi.item_code >= '{filters.get('from_no')}'"
	if filters.get("to_no") :
		conditions += f" and soi.item_code <= '{filters.get('to_no')}'"


	if filters.get("customer") :
		conditions += f" and so.customer = '{filters.get('customer')}'"
	if filters.get("item_code") :
		conditions += f" and soi.item_code = '{filters.get('item_code')}'"

	sql = f'''select so.name ,
	so.base_total_taxes_and_charges , so.delivery_date , so.transaction_date , 
	so.customer , so.cost_center , so.set_warehouse ,
	so.total , so.discount_amount  as final_discount_amount,so.base_grand_total , so.total_taxes_and_charges ,
	so.total_taxes_and_charges , soi.item_code , soi.item_name , soi.qty ,soi.rate , soi.discount_amount ,
	ST.sales_person 
	from 
		`tabSales Order` so 
	inner join 
		`tabSales Order Item` soi
	on 
		so.name = soi.parent 
	LEFT JOIN 
		`tabSales Team` ST
	ON 
		so.name = ST.parent
	where so.docstatus = 1 and {conditions}
	order by so.name desc
	'''
	data = frappe.db.sql(sql , as_dict = 1)

	final_data = []
	for row in data :
		doc = frappe.get_list("Purchase Receipt Item", 
							filters={"item_code": row['item_code']}, 
							fields=["rate"], 
							order_by="creation DESC", 
							limit=1)
		if doc:
			row["last_purchase_receipt"] = doc[0].rate
		else:
			row["last_purchase_receipt"] = 0.0
		row["diffrance"] = row["rate"] - row["last_purchase_receipt"]
		row["diffrance_percentage"] = row["diffrance"] / 100

		row["total_profit"] =row["rate"] - (row["qty"]* row["last_purchase_receipt"])
		if not row["last_purchase_receipt"] == 0.0 :
			row["percentage_profit"] =str((row["discount_amount"]- row["last_purchase_receipt"]) /( row["last_purchase_receipt"] ) ) + "%" 
		final_data.append(row)

		dict1={}
		dict1["name"] =  _("Total")
		dict1["rate"] = row["total"]
		final_data.append(dict1)

		dict1={}
		dict1["name"] =  _("Additional Discount Amount")
		dict1["rate"] = row["final_discount_amount"]
		final_data.append(dict1)

		dict1={}
		dict1["name"] =  _("Grand Total")
		dict1["rate"] = row["base_grand_total"]
		final_data.append(dict1)

		dict1={}
		dict1["name"] =  _("Total Taxes and Charges")
		dict1["rate"] = row["total_taxes_and_charges"]
		final_data.append(dict1)

		dict1={}
		dict1["name"] =  _("Grand Total")
		dict1["rate"] = row["base_grand_total"]
		final_data.append(dict1)

		dict1={}
		dict1["name"] =  _("Grand Total")
		dict1["rate"] = row["base_grand_total"]
		final_data.append(dict1)


	return final_data

def get_columns():
	return[
			{
				"label": _("Sales Order"),
				"fieldname": "name",
				"fieldtype": "Link",
				"options": "Sales Order",
				"width": 120,
			},
			{
				"label": _("Sales Person"),
				"fieldname": "sales_person",
				"fieldtype": "Link",
				"options": "Sales Person",
				"width": 120,
			},			{
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 120,
			},
			{
				"label": _("Item"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 120,
			},
			{
				"label": _("Item Name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 120,
			},
			{
				"label": _("Quantity"),
				"fieldname": "qty",
				"fieldtype": "Float",
				"width": 90,
			},
			{
				"label": _("Rate"),
				"fieldname": "rate",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			},
			{
                "label": "Cost Center",
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "insert_after": "base_amount",
                "options": "Cost Center",
            },
			{
				"label": _("Warehouse"),
				"fieldname": "set_warehouse",
				"fieldtype": "Link",
				"options": "Warehouse",
				"width": 100,
			},
			{
				"label": _("Discount Amount"),
				"fieldname": "discount_amount",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			},
			{
				"label": _("Last Purchase Receipt"),
				"fieldname": "last_purchase_receipt",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			},
			{
				"label": _("Diffrance Between rate and Last Purchase Receipt"),
				"fieldname": "diffrance",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			},
			{
				"label": _("Diffrance Percentage"),
				"fieldname": "diffrance_percentage",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			},
			{
				"label": _("Total Profit"),
				"fieldname": "total_profit",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			},
			{
				"label": _("Percentage Profit"),
				"fieldname": "percentage_profit",
				"fieldtype": "Data",
				"width": 150,
			},
	]