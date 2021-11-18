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
    except Exception as e : 
        pass
        # frappe.msgprint(str(e))






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
















