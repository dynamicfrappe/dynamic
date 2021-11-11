import frappe
import os
import json
def after_install():
	print("+dynamic")
	try:
		frappe.db.sql("""delete from tabWorkspace where name in ("HR","Loans","Payroll","Quality","Projects","Support")""")
		frappe.db.commit()
		frappe.db.sql("""delete from tabDocType where module='Loan Management'""")
		frappe.db.commit()
		frappe.db.sql("""delete from `tabModule Def` where name='Loan Management'""")
		frappe.db.commit()
		# frappe.db.sql("""delete from tabDocType where module='Payroll'""")
		# frappe.db.commit()
		frappe.db.sql("""delete from tabDocType where module="Payroll" and name!='Salary Component'""")
		frappe.db.commit()
		# frappe.db.sql("""delete from tabDocType where module='Projects'""")
		# frappe.db.commit()
		# frappe.db.sql("""delete from `tabModule Def` where name='Projects'""")
		# frappe.db.commit()
		print("+del module.text")
		#### after that del them from module
		a_file = open("../apps/erpnext/erpnext/modules.txt", "r")
		lines = a_file.readlines()
		a_file.close()
		new_file = open("../apps/erpnext/erpnext/modules.txt", "w")
		for line in lines:
			if line.strip("\n") !="Loan Management":
				new_file.write(line)
		new_file.close()
		install_uom()
	except Exception as e:
		print(e)
		pass


def install_uom():
	file_path = "../apps/dynamic/dynamic/MasterData/UnitTypes.json"
	with open(file_path) as f:
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