import frappe
from frappe import _


def validate(self , event):
    validate_items(self)

def before_submit(self , event):
   check_brand_for_customer(self)
   
def validate_items(self):
    for item in self.items :
        if item.brand != self.brand:
            frappe.throw(_("Brand of <b>{0}</b> should be <b>{1}</b>").format(item.item_code , self.brand))


def check_brand_for_customer(self):
   if frappe.db.exists("Sales Invoice", {"customer": self.customer ,"brand" :self.brand , "status":"Draft"}):
       frappe.throw(_("There are open sales invoice for <b>{0}</b> with the same <b>{1}</b>").format(self.customer, self.brand))
