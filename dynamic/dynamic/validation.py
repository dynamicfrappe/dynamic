import frappe
from frappe import _
# Terra Domain required 
from dynamic.terra.landed_cost import validate_cost
DOMAINS = frappe.get_active_domains()

def validate_landed_cost(doc,*args,**kwargs):
    ''' Add domain to run this customization  '''
    if 'Terra' in DOMAINS:
        validate_cost(doc)
