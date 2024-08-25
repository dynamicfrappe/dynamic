# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_data(filters):
	conditions = " 1=1 "
	if filters.get("from_date"):
		conditions += " AND `tabDelivery Note`.creation >= '%s' "%(filters.get("from_date"))
	if filters.get("to_date"):
		conditions += " AND `tabDelivery Note`.creation <= '%s' "%(filters.get("to_date"))
	if filters.get("doctor"):
		conditions += " AND `tabDelivery Note`.doctor LIKE '%{0}%' ".format(filters.get("doctor"))
	if filters.get("customer"):
		conditions += " AND `tabDelivery Note`.customer = '%s' "%(filters.get("customer"))
	if filters.get("surgery"):
		conditions += " AND `tabDelivery Note`.surgery LIKE '%%%s%%' "%(filters.get("surgery"))
	if filters.get("branch"):
		conditions += " AND `tabDelivery Note`.branch LIKE '%%%s%%' "%(filters.get("branch"))
	# if filters.get("customer"):
	# 	conditions += " AND `tabDelivery Note`.customer = '%s' "%(filters.get("customer"))
	if filters.get("warehouse"):
		print(filters)
		warehouse = "', '".join(filters.get("warehouse"))
		conditions += f" AND `tabDelivery Note`.set_warehouse IN ('{warehouse}')"
	if filters.get("item_group") :
		item_group = "', '".join(filters.get("item_group"))
		conditions += f" AND `tabItem`.item_group IN ('{item_group}')"
		

	sql = f"""
	SELECT `tabDelivery Note`.name
	,`tabDelivery Note`.doctor
	,`tabDelivery Note`.posting_date
	,`tabDelivery Note`.customer
	,`tabDelivery Note`.branch
	,`tabDelivery Note`.surgery
	,`tabCustomer`.customer_name 
	,`tabDelivery Note Item`.item_code
	,`tabDelivery Note Item`.item_name
	,`tabDelivery Note Item`.incoming_rate
	,`tabDelivery Note Item`.price_list_rate
	,`tabItem`.item_group
	,`tabDelivery Note Item`.qty
	,`tabDelivery Note Item`.warehouse
	FROM `tabDelivery Note`
	INNER JOIN `tabDelivery Note Item` 
	ON `tabDelivery Note`.name=`tabDelivery Note Item`.parent
	Inner JOIN `tabCustomer` 
	ON `tabDelivery Note`.customer=`tabCustomer`.name
	INNER JOIN `tabItem` ON `tabDelivery Note Item`.item_code = `tabItem`.item_code
	WHERE  `tabDelivery Note`.docstatus<>2 AND {conditions}
	"""
	result = frappe.db.sql(sql,as_dict=1)
	return result

def get_columns(filters):
	columns = [
		{
			"label": _("Name"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options":"Delivery Note",
			"width": 150
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Doctor"),
			"fieldname": "doctor",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Service"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Service Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Service Group"),
			"fieldname": "item_group",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Incoming Rate"),
			"fieldname": "incoming_rate",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Price List Rate"),
			"fieldname": "price_list_rate",
			"fieldtype": "Currency",
			"width": 150
		},
		
		{
			"label": _("QTY"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options":"Warehouse",
			"width": 150
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Data",
			"width": 150
		},
		
		{
			"label": _("Surgery"),
			"fieldname": "surgery",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 150
		},
		# {
		# 	"label": _("To Warehouse"),
		# 	"fieldname": "to_warehouse",
		# 	"fieldtype": "Link",
		# 	"options": "Warehouse",
		# 	"width": 150
		# },
		
		
		# {
		# 	"label": _("QTy"),
		# 	"fieldname": "qty",
		# 	"fieldtype": "Float",
		# 	"width": 150
		# },
		# {
		# 	"label": _("Price"),
		# 	"fieldname": "basic_rate",
		# 	"fieldtype": "Currency",
		# 	"width": 150
		# },
		# {
		# 	"label": _("Total Amount"),
		# 	"fieldname": "amount",
		# 	"fieldtype": "Currency",
		# 	"width": 150
		# },
		
		
		
	]
	
	return columns