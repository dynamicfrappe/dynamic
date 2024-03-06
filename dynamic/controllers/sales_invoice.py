import frappe
from frappe import _

Domains=frappe.get_active_domains()

def validate(self , event):
    if "Lormed" in Domains :
        validate_items(self)
    
    
def before_submit(self , event):
    if "Lormed" in Domains  and not self.ignore_validation: #and not self.ignore_validation
        check_open_sales_invoices(self)
    if "Qaswaa" in Domains :
        submit_invoice(self)

def validate_items(self):
    for item in self.items :
        if item.brand != self.brand:
            frappe.throw(_("Brand of <b>{0}</b> should be <b>{1}</b>").format(item.item_code , self.brand))

def check_open_sales_invoices(self):
   if frappe.db.exists("Sales Invoice", {"customer": self.customer ,"brand" :self.brand , "docstatus" : 1 ,"outstanding_amount" : [">" ,1.00] , "name" :["!=", self.name]}):
       frappe.throw(_("There are open sales invoice for <b>{0}</b> with the same brand <b>{1}</b>").format(self.customer, self.brand))

def submit_invoice(self):
    sales_document = frappe.new_doc("Sales Document States")
    sales_document.posting_date = self.posting_date
    sales_document.invoice_type = self.doctype
    sales_document.invoice_name = self.name
    # sales_document.shipping_company = self.company
    sales_document.Customer = self.customer
    sales_document.customer_name = self.customer_name
    sales_document.grand_total = self.grand_total
    sales_document.insert()


