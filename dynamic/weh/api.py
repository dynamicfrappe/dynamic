import frappe
import requests
import json
from frappe import _

# url : /api/method/dynamic.weh.api.create_customer

# from erpnext.stock.doctype.stock_entry.stock_entry import  set_stock_entry_type,set_missing_values
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, comma_or, cstr, flt, format_time, formatdate, getdate, nowdate


@frappe.whitelist()
def customer(*args, **kwargs):
	try :
		data = json.loads(frappe.request.data)
	except Exception as e :
		frappe.local.response['message'] = f"Error Accourd   {e}"
		frappe.local.response['http_status_code'] = 400 
		return
	# validaion
	if not data.get("customer_name"):
		frappe.local.response['message'] = "Customer name required"
		frappe.local.response['http_status_code'] = 400 
		return
	if not data.get("remote_id"):
		frappe.local.response['message'] = "remote id required"
		frappe.local.response['http_status_code'] = 400 
		return

	if not frappe.db.exists("Customer",{"remote_id":data.get("remote_id")}):
		customer = frappe.new_doc("Customer")
	if  frappe.db.exists("Customer",{"remote_id":data.get("remote_id")}):    
		customer = frappe.get_doc("Customer",{"remote_id":data.get("remote_id")})
	customer.customer_name = data.get("customer_name")
	customer.customer_group = "All Customer Groups"
	customer.territory = "All Territories"
	customer.remote_id = data.get("remote_id")
	customer.branch = data.get("branch") or " "
	customer.doctor = data.get("doctor") or " "
	customer.branch = data.get("surgery") or " "
	try:
		customer.save()
		frappe.local.response['message'] = customer.name
		frappe.local.response['http_status_code'] = 200 
		return
	except Exception as ex:
		frappe.local.response['message'] = str(ex)
		frappe.local.response['http_status_code'] = 400 
		return


@frappe.whitelist()
def get_consumables():
	try :
		data = json.loads(frappe.request.data)
	except Exception as e :
		frappe.local.response['message'] = f"Error Accourd   {e}"
		frappe.local.response['http_status_code'] = 400 
		return
	# if not data.get("date"):
	#     frappe.local.response['message'] = "Customer name required"
	#     frappe.local.response['http_status_code'] = 400 
	#     return
	if not data.get("remote_id"):
		frappe.local.response['message'] = "remote id required"
		frappe.local.response['http_status_code'] = 400 
		return
	if not frappe.db.exists("Customer",{"remote_id":data.get("remote_id")}):
		frappe.local.response['message'] = "CUSTOMER NOT FOUND !"
		frappe.local.response['http_status_code'] = 400 
	# if  frappe.db.exists("Customer",{"remote_id":data.get("remote_id")}):    
	customer = frappe.get_doc("Customer",{"remote_id":data.get("remote_id")})

	d_sql = f""" select name from `tabDelivery Note` WHERE customer='{customer.name}' """
	if data.get("date") :
		date =  data.get("date")
		d_sql = d_sql +f"and posting_date =date('{date}')"

		get_name= frappe.db.sql(d_sql ,as_dict= 1)
		if get_name and len(get_name) > 0  :
			name = get_name[0].get("name")
			if name :
				fileds = ""
				if data.get("branch") :
				   fileds =  fileds + f""" branch = '{data.get("branch") }' ,"""
				if data.get("doctor") :
				   fileds =  fileds + f""" doctor = '{data.get("doctor") } ',"""
				if data.get("surgery") :
				   fileds =  fileds + f""" surgery = '{data.get("surgery") }' ,"""

				
				frappe.db.sql (f"""
				UPDATE `tabDelivery Note` SET {fileds[0:-1]}
				WHERE name ='{name}'  
				""")
				frappe.db.commit()
	try :
		delvery_note = frappe.db.sql(f""" 
		select item_name , qty , rate , price_list_rate ,base_amount as amount from `tabDelivery Note Item` WHERE parent in ({d_sql})
		""",as_dict=1)


		frappe.local.response['message'] =delvery_note
		frappe.local.response['http_status_code'] = 200
		# return delvery_note
	except Exception as E :
		frappe.local.response['message'] = f"ERROR ! {E}"
		frappe.local.response['http_status_code'] = 400


def get_sum_consumables():
	try :
		data = json.loads(frappe.request.data)
	except Exception as e :
		frappe.local.response['message'] = f"Error Accourd   {e}"
		frappe.local.response['http_status_code'] = 400 
		return
	# if not data.get("date"):
	#     frappe.local.response['message'] = "Customer name required"
	#     frappe.local.response['http_status_code'] = 400 
	#     return
	if not data.get("remote_id"):
		frappe.local.response['message'] = "remote id required"
		frappe.local.response['http_status_code'] = 400 
		return
	if not frappe.db.exists("Customer",{"remote_id":data.get("remote_id")}):
		frappe.local.response['message'] = "CUSTOMER NOT FOUND !"
		frappe.local.response['http_status_code'] = 400 
	# if  frappe.db.exists("Customer",{"remote_id":data.get("remote_id")}):    
	customer = frappe.get_doc("Customer",{"remote_id":data.get("remote_id")})

	d_sql = f""" select name from `tabDelivery Note` WHERE customer='{customer.name}' """
	if data.get("date") :
		date =  data.get("date")
		d_sql = d_sql +f"and posting_date =date('{date}')"
	try :
		delvery_note = frappe.db.sql(f""" 
		select SUM( base_amount) as amount from `tabDelivery Note Item` WHERE parent in ({d_sql})
		""",as_dict=1)
		frappe.local.response['message'] =delvery_note
		frappe.local.response['http_status_code'] = 200
		# return delvery_note
	except Exception as E :
		frappe.local.response['message'] = f"ERROR ! {E}"
		frappe.local.response['http_status_code'] = 400



@frappe.whitelist()
def make_stock_in_entry(source_name, target_doc=None):
	# frappe.throw('test')
	def set_missing_values(source, target):
		target.set_stock_entry_type()
		target.set_missing_values()
		target.from_warehouse=source.to_warehouse

	def update_item(source_doc, target_doc, source_parent):
		target_doc.t_warehouse = ""

		if source_doc.material_request_item and source_doc.material_request:
			add_to_transit = frappe.db.get_value("Stock Entry", source_name, "add_to_transit")
			if add_to_transit:
				warehouse = frappe.get_value(
					"Material Request Item", source_doc.material_request_item, "warehouse"
				)
				target_doc.t_warehouse = warehouse

		target_doc.s_warehouse = source_doc.t_warehouse
		target_doc.qty = source_doc.qty - source_doc.transferred_qty

	doclist = get_mapped_doc(
		"Stock Entry",
		source_name,
		{
			"Stock Entry": {
				"doctype": "Stock Entry",
				"field_map": {
						"name": "outgoing_stock_entry",
					},
				"validation": {"docstatus": ["=", 1]},
			},
			"Stock Entry Detail": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"name": "ste_detail",
					"parent": "against_stock_entry",
					"serial_no": "serial_no",
					"batch_no": "batch_no",
				},
				"postprocess": update_item,
				"condition": lambda doc: flt(doc.qty) - flt(doc.transferred_qty) > 0.01,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist


@frappe.whitelist()
def get_roles_hidden_field(field_hide=None,field_empty=None):
	user_roles = frappe.get_roles()
	warehouse_settings = frappe.get_single("Warehouse Setting")
	empty = True if warehouse_settings.get(field_empty) in  user_roles else False
	hide = True if warehouse_settings.get(field_hide) in  user_roles else False
	return {"hide":hide,"empty":empty}
   

