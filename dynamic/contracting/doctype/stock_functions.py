
from __future__ import unicode_literals
from frappe import _
import frappe 




#stock entry over write 

# 1- find if contatracting in installed domains 
DOMAINS = frappe.get_active_domains()
@frappe.whitelist()
def fetch_contracting_data(*args , **kwargs ):
    if 'Contracting' in DOMAINS : 
        return True
    else :
         return False

@frappe.whitelist()
def stock_entry_setup(comparison , *args ,**kwargs):
    data = frappe.db.sql(""" SELECT `tabItem`.item_code  FROM  `tabItem`
    inner Join
    `tabComparison Item` on `tabItem`.name = `tabComparison Item`.clearance_item
    WHERE 
    `tabComparison Item`.parent = '%s' """%comparison )
    item_list = []
    for i in data :
        item_list.append(i[0])
    return (item_list)