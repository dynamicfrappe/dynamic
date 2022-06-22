from email import message
from logging import exception
from pydoc import importfile
# from tkinter import E
import json
from pathlib import Path
import os
import frappe
import os





MasterDataPath = "../apps/dynamic/dynamic/MasterData/"
def install_e_invoice():
	try:
		install_uom()
	except :
		pass
	try :
		install_Country()
	except Exception as e:
		pass
		# frappe.msgprint(str(e))
	try:
		sales_invoice_script()
	except:
		pass
	try:
		import_activity_code()
	except Exception as e:
		handle_err(e)
	try:
		import_tax_types()
	except:
		pass
	






def install_uom():
	file_path = "UnitTypes.json"
	with open(MasterDataPath+file_path) as f:
		data = json.load(f)
		for i in data :
			try:
				frappe.get_doc({
					"doctype":"UOM",
					"uom_name":i.get("code"),
					"english_description":i.get("desc_en"),
					"arabic_description":i.get("desc_ar"),
				}).insert()
			except Exception as e:
				pass
				# print (str(e))


def install_Country():
	file_path = "CountryCodes.json"
	with open(MasterDataPath+file_path) as f:
		data = json.load(f)
		# print (data)
		for i in data :
			# print (i)
			# try:
				frappe.get_doc({
					"doctype":"Country Code",
					"code":i.get("code"),
					"english_description":i.get("Desc_en"),
					"arabic_description":i.get("Desc_ar"),
				}).insert()
				# print (str(i.get("desc_en")))
			# except Exception as e:
				# pass
				# print (str(e))

def sales_invoice_script():
	name = "Sales Invoice-Form"
	if frappe.db.exists("Client Script", name):
		pass
	else:

		doc = frappe.new_doc("Client Script")
		print("+ from add script")
		doc.dt = "Sales Invoice"
		doc.view = "Form"
		doc.enabled = 1
		doc.script = """

				frappe.ui.form.on('Sales Invoice', {
				refresh(frm) {
					if(frm.doc.docstatus==1 && frm.doc.is_send == 0){
								frm.add_custom_button(__("POST"), function() {
									frappe.call({
										method:"dynamic.e_invoice.sales_invoice_fun.post_sales_invoice",
										args:{
											"invoice_name":frm.doc.name
										}
									})
								})
								}
			
				}
			})

				"""
		doc.save()





path_file = "dynamic/dynamic/public/tax_types/"
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

path_fiels = ["sinv1.json","sinv2.json","sinv3.json"]
@frappe.whitelist()
def import_tax_types():
	try :
		for fname in path_fiels:
			taxable = (fname=="sinv1.json")
			file_path = path_file + fname
			file_path =  os.path.join(BASE_DIR,file_path)
			main_file = open(file_path)
			data_js = json.load(main_file)

			insert_data(data_js,taxable)
	except Exception as e:
		 handle_err(e)

def insert_data(data_js,taxable=0):
	try :
		for  data in data_js:
<<<<<<< HEAD
			tax_type = frappe.new_doc("Tax Types")
			tax_type.code = data["Code"] if data["Code"] else ''
			tax_type.desc_en = data["Desc_en"] if data["Desc_en"] else ''
			tax_type.desc_ar = data["Desc_ar"] if data["Desc_ar"] else ''
			tax_type.taxtypereference = data.get("TaxtypeReference","")
			tax_type.taxable = taxable
			tax_type.save()
=======
			if not	frappe.db.exists("Tax Types", {"code": data["Code"]}):
				tax_type = frappe.new_doc("Tax Types")
				tax_type.code = data["Code"] if data["Code"] else ''
				tax_type.desc_en = data["Desc_en"] if data["Desc_en"] else ''
				tax_type.desc_ar = data["Desc_ar"] if data["Desc_ar"] else ''
				tax_type.fixed_amount = data.get("fixed_amount","")
				tax_type.taxtypereference = data.get("TaxtypeReference","")
				tax_type.save()
>>>>>>> 88b9b5827fcd0bab9cd2cf6464ad28e11e3a2c2f
		return 'done'
	except Exception as e:
		 handle_err(e)


path_file_ac = "dynamic/dynamic/public/activity_code/"
BASE_DIR_ac = Path(__file__).resolve().parent.parent.parent.parent
@frappe.whitelist()
def import_activity_code():
	try:
		file_path = path_file_ac + 'activity_code.json'
		file_path =  os.path.join(BASE_DIR_ac,file_path)
		main_file_data = open(file_path)
		data_js = json.load(main_file_data)
		insert_activity_code_data(data_js)
	except Exception as e:
		 handle_err(e)

	
def insert_activity_code_data(data_js):
	try :
		for data in data_js:
			if not	frappe.db.exists("Activity Code", {"code": data["code"]}):
				activity_code = frappe.new_doc("Activity Code")
				activity_code.code = data["code"] if data["code"] else ''
				activity_code.desc_en = data["Desc_en"] if data["Desc_en"] else ''
				activity_code.desc_ar = data["Desc_ar"] if data["Desc_ar"] else ''
				activity_code.save()
	except exception as e:
		 handle_err(e) 







def handle_err(e):
	error = frappe.new_doc("Error Log")
	error.error = str(e)
	error.save() 


