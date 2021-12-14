import frappe
import os
import json





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





def install_uom():
	file_path = "UnitTypes.json"
	with open(MasterDataPath+file_path) as f:
		data = json.load(f)
		# print (data)
		for i in data :
			# print (i)
			try:
				frappe.get_doc({
					"doctype":"UOM",
					"uom_name":i.get("code"),
					"english_description":i.get("desc_en"),
					"arabic_description":i.get("desc_ar"),
				}).insert()
				# print (str(i.get("desc_en")))
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















