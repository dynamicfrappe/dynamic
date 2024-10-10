import frappe
from frappe import _
import requests
import json
from dynamic.api_method.auth import get_token
Domains=frappe.get_active_domains()

@frappe.whitelist(allow_guest = True)
def before_validate(self, event):
    if 'Logistics' in Domains :
        get_numbers(self)
        filter_with_numbers(self)

def get_numbers(self):
    if self.phone_nos :
        phones = " ".join(str(number.phone) for number in self.phone_nos)
        return phones

def filter_with_numbers(self):
    phones = get_numbers(self)
    if self.links :
        for link in self.links:
            if link.link_doctype == 'Lead':
                    print("ffffff")
                    frappe.db.set_value('Lead',link.link_name,'mobile',f'{phones}')
                    (f""" UPDATE `tabLead` SET 
                        mobile='{phones}' 
                        WHERE name = "{link.link_name}" """)
                    frappe.db.commit()