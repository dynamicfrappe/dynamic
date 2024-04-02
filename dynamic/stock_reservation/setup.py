import frappe 



def setup(*arg ,**kargs):
    create_domain()


def create_domain():
    if not frappe.db.exists("Domain","Stock Reservation"):
        doc = frappe.new_doc("Domain")
        doc.domain = "Stock Reservation"
        doc.save()
