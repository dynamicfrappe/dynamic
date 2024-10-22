import frappe
from frappe import _
import requests
import json
from dynamic.api_method.auth import get_token
Domains=frappe.get_active_domains()

@frappe.whitelist(allow_guest = True)
def before_validate(self, event):
    if 'Logistics' in Domains :
        # validate_numbers(self)
        get_numbers(self)
        filter_with_numbers(self)
        set_numbers(self)

def get_numbers(self):
    if self.numbers :
        phones = " ".join(str(number.number) for number in self.numbers)
        return phones

def filter_with_numbers(self):
    phones = get_numbers(self)
    if self.links :
        for link in self.links:
            if link.link_doctype == 'Lead':
                    frappe.db.set_value('Lead',link.link_name,'mobile',f'{phones}')
                    (f""" UPDATE `tabLead` SET 
                        mobile='{phones}' 
                        WHERE name = "{link.link_name}" """)
                    frappe.db.commit()

def set_numbers(self):
    for no in self.phone_nos :
        if not frappe.db.exists({"doctype": "Number", "number": no.phone}):
            self.append("numbers" ,{"number" : no.phone})

def validate_numbers(self):
    list = []
    for number in self.phone_nos :
        if number.phone in list :
            frappe.throw("This number has been added in Contact Numbers")
        list.append(number.phone)