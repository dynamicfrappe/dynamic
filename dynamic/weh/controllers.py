import frappe 
from frappe import _, throw 


@frappe.whitelist(allow_guest=False)
def get_defaulte_source_warehouse(*args ,**kwargs) :
    
    warehouse = frappe.db.sql(f"""select parent FROM `tabWarehouse User` 
    WHERE  user= "{frappe.get_user().name}" 
    """
   )
    li  =[i[0] for i in warehouse]
    
    return li





@frappe.whitelist(allow_guest=False)
def user_can_edit(doc , *args, **kwargs) :

    pass
