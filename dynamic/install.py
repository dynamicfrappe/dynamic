import frappe
import os
def after_install():
	print("+dynamic")
	try:
		frappe.db.sql("""delete from tabWorkspace where name in ("HR","Loans","Payroll")""")
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
	except Exception as e:
		print(e)
		pass