import frappe
active_domains = frappe.get_active_domains()

def on_cancel(self , event):
    if "Terra" in active_domains:
        if self.quotation :
            supplier_quotation = frappe.get_doc("Supplier Quotation" , self.quotation)
            supplier_quotation.cancel()