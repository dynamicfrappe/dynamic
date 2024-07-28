import frappe

def on_cancel(self , event):
    if self.quotation :
        supplier_quotation = frappe.get_doc("Supplier Quotation" , self.quotation)
        supplier_quotation.cancel()