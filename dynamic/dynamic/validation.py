import frappe
from frappe import _
# Terra Domain required 
from dynamic.terra.landed_cost import validate_cost
from dynamic.terra.sales_invoice import check_return_account
DOMAINS = frappe.get_active_domains()

def validate_landed_cost(doc,*args,**kwargs):
    ''' Add domain to run this customization  '''
    if 'Terra' in DOMAINS:
        validate_cost(doc)
    

def validate_sales_invoice(doc,*args,**kwargs):
    if 'Terra' in DOMAINS:
        check_return_account(doc)