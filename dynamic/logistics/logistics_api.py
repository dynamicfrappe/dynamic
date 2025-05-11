import frappe
from frappe.utils import date_diff , now
DOMAINS = frappe.get_active_domains()


def check_data_remaining():
    if 'Logistics' in DOMAINS: 
        containers = frappe.db.get_list(
                    "PO Container",
                    filters={
                        "status": "Ordered",
                    },
                    pluck = "name")
        for container in containers :
            container = frappe.get_doc("PO Container" , container)
            differance = date_diff( container.arrived_date ,now() )
            container.remaining_date = f'{differance}' + " days"
            if differance < 0 :
                container.status = "Overdue"
            container.save()
            
def check_data_remaining_before_save(doc, method):
    if 'Logistics' in DOMAINS: 
        differance = date_diff( doc.arrived_date ,now() )
        doc.remaining_date = f'{differance}' + " days"
        if differance < 0 :
            doc.status = "Overdue"