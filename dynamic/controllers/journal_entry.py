import frappe
from frappe import _

Domains=frappe.get_active_domains()

def before_submit_journal_entry(self , event):
    if "Rehab"  in Domains :
        set_claiming_entry(self)

def set_claiming_entry(self):
    if self.installment_entry :
        installment_entry = frappe.get_doc("installment Entry", self.installment_entry)
        if installment_entry.status != "Paid"  :
            installment_entry.is_clamed = 1
            installment_entry.append("claiming_entry" , {"type" :self.doctype , "document" :self.name})
            installment_entry.save()