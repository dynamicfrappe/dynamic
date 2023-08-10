


import frappe
from frappe import _


@frappe.whitelist()
def delivery_note_before_submit(delivery_doc , *args , **kwargs):
    for row in delivery_doc.items:
        if row.against_sales_order:
            #**main phase
            #1- check sales order is reserved check box enabled
            #2- if not reservation -> validate avail qty in stock and reserved qty for warehouse (common method used also if SO reserved)
            #3- if SO reserved check (common method used a)
            ...
        elif row.against_sales_invoice:
            #-loop over items get againts_sales order
            #-
            ...
        #! check if available qty in stock and reservation
        try:
            if row.reservation:
                #?** if row hase reservation name : check reservation qty = row qty then go on
                get_reserv_qty = frappe.db.sql(f"""  
                SELECT qty FROM `tabReservation Warehouse` WHERE parent='{row.reservation}'
                """) 
                if row.qty != get_reserv_qty[0].qty:
                    frappe.throw(_("Avail QTY Is {0} In Reservation Not Equal To Item {1} QTY").format(get_reserv_qty[0].qty,row.item_code))  
                #** if qty available minus reservation qty with deliverd qty
                pass
        except Exception as e:
            frappe.db.rollback()
        if not row.reservation:
            #?**  if no reservation  check actual qty in stock - reservation qty >= row.qty
            pass
        frappe.errprint('test')


def check_each_row_vaild_qty():
    ...

#"dynamic.reservation.reservation_api.check_valid_item_qty"
def check_valid_item_qty():
    ...

def validate_decorator(doc,invoice=None):
    ...

