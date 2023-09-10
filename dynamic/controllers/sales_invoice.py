import frappe
from frappe import _


def validate(self , event):
    validate_items(self)

def before_submit(self , event):
   check_open_sales_invoices(self)

def validate_items(self):
    for item in self.items :
        if item.brand != self.brand:
            frappe.throw(_("Brand of <b>{0}</b> should be <b>{1}</b>").format(item.item_code , self.brand))

def check_open_sales_invoices(self):
   if frappe.db.exists("Sales Invoice", {"customer": self.customer ,"brand" :self.brand , "docstatus" : 1 ,"outstanding_amount" : [">" ,1.00] , "name" :["!=", self.name]}):
       frappe.throw(_("There are open sales invoice for <b>{0}</b> with the same brand <b>{1}</b>").format(self.customer, self.brand))
