import frappe
from frappe import _


DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def validate(self ,event):
    print(DOMAINS)
    if 'Al wefak' in DOMAINS:
        valid_qty(self)



def valid_qty(self):#noha
             operations = self.get('operations')
             workorder_qty = self.get('qty')
             for operation in operations: 
                print(operation.workstation)
                workstation_doc = frappe.get_doc("Workstation", operation.workstation)
                if workstation_doc:
                   min_qty =int(workstation_doc.min_qty or 0)
                   print(min_qty)
                if min_qty>workorder_qty  &  min_qty>0:
                       frappe.msgprint(_(f"Work order Quantity is less than quantity in workstation :{operation.workstation} minimum quantity is {min_qty}"))
                        