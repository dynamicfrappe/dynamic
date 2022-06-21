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




@frappe.whitelist()
def get_query_type (*args,**kwargs):
	return[[ "Purchase Invoice"],["Payment Entry"] , ["Journal Entry"]]

@frappe.whitelist()
def get_purchase_items(invoice=None , *args , **kwargs):


	invoices = frappe.db.sql("""SELECT  p.parent  FROM 
                                `tabPurchase Invoice Item`  p
								inner join   
                                `tabItem`  a 
                                inner join 
                                `tabPurchase Invoice` as c
                                on p.item_code = a.item_code and c.name = p.parent
								WHERE a.is_stock_item = 0 and c.docstatus = 1 
								group by p.parent   """)

 
	return invoices

@frappe.whitelist()
def get_active_domain():
    if 'Terra' in DOMAINS:
        return True
    else :
        return False
    
def validate_item_code(doc,*args,**kwargs):
    if 'Terra' in DOMAINS:
        if doc.is_new():
            create_item_serial_doc(doc)