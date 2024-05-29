import frappe 



@frappe.whitelist()
def create_domain(*args , **kwargs) :
    if not frappe.db.exists("Domain" , "Megaback") :
        megaback = frappe.new_doc("Domain")
        megaback.domain = "Megaback"
        megaback.save()
        frappe.db.commit()
        print("Megaback Domain added ")