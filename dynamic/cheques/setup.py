
from frappe import _
import frappe
from dynamic.dynamic_accounts.setup import add_properties
def install():
    try:
        add_properties()
    except Exception as e:
        frappe.throw(_(str(e)))
    pass