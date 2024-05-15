# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 

# get last purchase price 
from dynamic.qaswaa.utils.qaswaa_api import get_last_purchase_invoice_for_item_with_date
							
def execute(filters=None):
	columns, data =get_columns(filters), get_data(filters)
	return columns, data



def get_columns(filters=None) :

	"""
	 cols from 1 : 8 from tabItem 
	
	"""
	
	return [
				#1 
				{	"label": _("Item Code"),
					"fieldname": "item_code",
					"fieldtype": "Data",
					"width": 250,
				},
				#2
				{	"label": _("Item Name"),
					"fieldname": "item_name",
					"fieldtype": "Data",
					"width": 250,
				},
				#3
				{	"label": _("Warehouse"),
					"fieldname": "warehouse",
					"fieldtype": "Data",
					"width": 200,
				},
				#4
				{	"label": _("Item Group"),
					"fieldname": "item_group",
					"fieldtype": "Data",
					"width": 200,
				},
				#5
				{	"label": _("Tax Group"),
					"fieldname": "tax_group",
					"fieldtype": "Data",
					"width": 200,
				},
				#6
				{	"label": _("Material"),
					"fieldname": "material",
					"fieldtype": "Data",
					"width": 200,
				},
				#7 
				{	"label": _("Brand"),
					"fieldname": "brand",
					"fieldtype": "Data",
					"width": 200,
				},
				#8
				{	"label": _("Origin"),
					"fieldname": "origin",
					"fieldtype": "Data",
					"width": 200,
				},
				#9
				{	"label": _("Stock Qty"),
					"fieldname": "stock_qty",
					"fieldtype": "Data",
					"width": 200,
				},
				#10
				{	"label": _("valuation Rate"),
					"fieldname": "v_r",
					"fieldtype": "Data",
					"width": 200,
				},
				#11
				
				
				{	
     				"label": _("Last Purchase Price"),
					"fieldname": "l_p_p",
					"fieldtype": "Data",
					"width": 200,
				},
				#12
				
				{	"label": _("Last Purchase Price Date"),
					"fieldname": "l_s_p_date",
					"fieldtype": "Data",
					"width": 200,
				},
				#13
				{	"label": _("Total Cost"),
					"fieldname": "total_cost",
					"fieldtype": "Data",
					"width": 200,
				},
				#14
				{	"label": _("Total Purchase Price"),
					"fieldname": "total_p_p",
					"fieldtype": "Data",
					"width": 200,
				},


			]




def get_data(filters=None) :

	"""
	filters
		company
		date
		warehouse
		item_group
		tax_group
		origin
		brand
		warehouse_group
		material


	tables 
		`tabBin` 
		`tabItem` 

	
	"""
	filter_qyery = ""

	if filters.get("company") :
		filter_qyery = filter_qyery + f"""and warehouse.company = "{filters.get('company')}" """
	if filters.get("item_group") :
		filter_qyery = filter_qyery + f"""and item.item_group = "{filters.get('item_group')}" """
	if filters.get("warehouse") :
		filter_qyery = filter_qyery + f"""and bin.warehouse = "{filters.get('warehouse')}" """
	if filters.get("tax_group") :
		filter_qyery = filter_qyery + f"""and item.group_code = "{filters.get('tax_group')}" """
	if filters.get("origin") :
		filter_qyery = filter_qyery + f"""and item.origin = "{filters.get('origin')}" """
	if filters.get("brand") :
		filter_qyery = filter_qyery + f"""and item.brand = "{filters.get('brand')}" """
	if filters.get("material") :
		filter_qyery = filter_qyery + f"""and item.material = "{filters.get('material')}" """
	if filters.get("warehouse_group") :
		filter_qyery = filter_qyery + f"""
		and warehouse.parent_warehouse = "{filters.get('warehouse_group')}" 
		"""
	

	qery  = f"""
	SELECT 
	 item.item_code  ,
	 item.item_name , 
	 bin.warehouse  , 
	 item.item_group , 
	 item.group_code as tax_group , 
	 item.material as material , 
	 item.brand as brand , 
	 item.origin , 
	 bin.actual_qty  as stock_qty, 
	 bin.valuation_rate as v_r  ,
	 (bin.actual_qty *  bin.valuation_rate) as total_cost 
	FROM `tabBin` bin 
	Inner Join `tabItem`  item 
	ON bin.item_code = item.name  
	Inner Join `tabWarehouse`  warehouse  ON 
	bin.warehouse = warehouse.name
	 
	where 1=1 and warehouse.is_group =0 
	
	""" + filter_qyery

	

	

	data = frappe.db.sql(qery ,as_dict=1)

	respone = []
	for item in data :
		item["l_p_p"] , item['l_s_p_date'] = get_last_purchase_invoice_for_item_with_date(item.get("item_code"))
		item["total_p_p"] = float(item.get("stock_qty") or 0) *\
								float(item.get("l_p_p") or 0)
	return data