

from erpnext import get_default_company
import frappe
from frappe import _


def validate_delivery_notes_sal_ord(doc):

    # validate sales invocie linked with sales order 
    for line in doc.items :
        if not line.against_sales_order : 
            frappe.throw(_(f"""You can not add Delivery Note withou Sales Order 
                                Please Check item {line.item_name}"""))

    #check reservation 
    sales_order = frappe.get_doc('Sales Order',doc.items[0].against_sales_order)
    #close Item Reservation 
    for row in sales_order.items:
        frappe.db.set_value('Reservation',row.reservation,{
        'status': 'Closed',
    })
        