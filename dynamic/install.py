import frappe

def after_install():
	print("+dynamic")
	try:
		frappe.db.sql("""delete from tabWorkspace where name in ("HR","Loans","Payroll")""")
		frappe.db.commit()
		frappe.db.sql("""delete from tabDocType where module='Loan Management'""")
		frappe.db.commit()
		frappe.db.sql("""delete from `tabModule Def` where name='Loan Management'""")
		frappe.db.commit()
		frappe.db.sql("""delete from tabDocType where module='Payroll'""")
		frappe.db.commit()
		frappe.db.sql("""delete from `tabModule Def` where name='Payroll'""")
		frappe.db.commit()
	except:
		pass