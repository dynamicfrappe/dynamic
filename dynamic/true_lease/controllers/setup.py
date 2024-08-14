
import frappe 

@frappe.whitelist()
def create_domain(*args , **kwargs) :
    if not frappe.db.exists("Domain" , "True lease") :
        megaback = frappe.new_doc("Domain")
        megaback.domain = "True lease"
        megaback.save()
        frappe.db.commit()
        print("True lease Domain added ")
