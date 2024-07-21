

from erpnext import get_default_company
import frappe
from frappe import _

DOMAINS = frappe.get_active_domains()




@frappe.whitelist()
def validate_terra_delievery_not(doc ,*args ,**kwargs ) :
   if "Terra" in DOMAINS:
       for i in doc.items :
           item = frappe.get_doc("Item" , i.item_code)
           for uom in item.uoms :
               if uom.is_sub_uom  :
                   i.sub_uom = uom.uom
                   i.sub_uom_conversation_factor = uom.conversion_factor
                   i.qty_as_per_sub_uom = float(i.stock_qty or 1) / float(i.sub_uom_conversation_factor or 1)
def validate_delivery_notes_sal_ord(doc):
    # validate sales invocie linked with sales order 
    for line in doc.items :
        if not line.against_sales_order : 
            frappe.throw(_(f"""You can not add Delivery Note without Sales Order 
                                Please Check item {line.item_name}"""))
        if  not line.sales_order_approval : 
            frappe.throw(_(f"""You can not add Delivery Note without Sales Order Approver
                                Please Check item {line.item_name}"""))

    #check reservation 
    # for line in doc.items :
    #     reservation_name = frappe.db.get_value("Sales Order Item",line.so_detail,"reservation")
    #     frappe.db.set_value('Reservation',reservation_name,{
    #         'status': 'Closed',
    #     })
  
        