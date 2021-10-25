import frappe

def after_install():
	try:
		frappe.db.sql("""delete from tabWorkspace where name in ("HR","Loans","Payroll")""")
		frappe.db.commit()
	except:
		pass