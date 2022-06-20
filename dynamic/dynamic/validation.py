import frappe
from frappe import _
# Terra Domain required 
from dynamic.terra.landed_cost import validate_cost
from dynamic.terra.sales_invoice import check_return_account
from dynamic.terra.item import create_item_serial_doc
DOMAINS = frappe.get_active_domains()

def validate_landed_cost(doc,*args,**kwargs):
    ''' Add domain to run this customization  '''
    if 'Terra' in DOMAINS:
        validate_cost(doc)
    

def validate_sales_invoice(doc,*args,**kwargs):
    if 'Terra' in DOMAINS:
        check_return_account(doc)

def validate_item_code(doc,*args,**kwargs):
    if 'Terra' in DOMAINS:
        print("aaaaaaaaaaaaaaaaaaaaas ==============> ",doc.is_new())
        if doc.is_new():
            create_item_serial_doc(doc)
        #pass