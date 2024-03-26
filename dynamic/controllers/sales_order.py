



import frappe
from frappe import _
from frappe import _, bold
from dynamic.qaswaa.controllers.sales_order_api import validate_item_qty_reserved

Domains=frappe.get_active_domains()

def validate_sales_order(self , event):
    if "Qaswaa" in Domains :
        validate_item_qty_reserved(self,event)


def validate_sales_order_for_stock(self , event):
    if "Stock Reservation" in Domains:
        get_validation(self,event)


def on_submit(self , event):
    if "Stock Reservation" in Domains:
        creation_of_reseration(self , event)
    

    
 

def get_validation(self , *args, **kwargs):
    if frappe.db.get_single_value("Stock Settings" , "allow_partial_reservation"):
        items = self.get("items")
        for item in items:
            item_code = item.item_code
            qty = item.qty
            # uom = item.uom
            warehouse = item.warehouse
            bin_qty = frappe.db.get_value("Bin" , filters={"item_code":item_code, "warehouse":warehouse} , fieldname = 'actual_qty')
            reservation_qty = frappe.db.get_value("Stock Reservation Entry" , filters={"item_code":item_code, "warehouse":warehouse} , fieldname = 'reserved_qty')
            total_qty = bin_qty + (reservation_qty if reservation_qty else 0)
            if qty > total_qty:
                wanted_qty = float(qty) - float(total_qty)
                msg = f"""
                    Item Name {bold(item.item_code)} Need Qty {bold(wanted_qty)}<br>
                    """
                frappe.throw(msg)


def creation_of_reseration(self , *args , **kargs):
    items = self.get("items")
    for item in items:
        log = frappe.new_doc("Stock Reservation Entry")
        log.item_code = item.item_code
        log.warehouse = item.warehouse
        log.voucher_type = "Sales Order"
        log.voucher_no = self.name
        log.voucher_detail_no = item.name
        log.stock_uom = item.uom
        bin_qty = frappe.db.get_value("Bin" , filters={"item_code":item.item_code, "warehouse":item.warehouse} , fieldname = 'actual_qty')
        reservation_qty = frappe.db.get_value("Stock Reservation Entry" , filters={"item_code":item.item_code, "warehouse":item.warehouse} , fieldname = 'reserved_qty')
        total_qty = bin_qty + (reservation_qty if reservation_qty else 0)
        log.available_qty_to_reserve = get_all_qty_reserved(item.item_code , item.warehouse)
        log.reserved_qty = float(item.qty) * float(item.conversion_factor)
        log.voucher_qty = item.qty 
        log.company = self.company
        log.status = "Reserved"
        # log.save()
        log.insert()

                

def convertor( item_code , uom ):
    item = frappe.get_doc("Item" , item_code)
    conversion_factor = 1
    uoms = item.get("uoms")
    for i in uoms:
        if uom == i.uom:
            conversion_factor = i.conversion_factor
    return conversion_factor



def get_all_qty_reserved (item_code, warehouse):
    item_reserved = frappe.db.sql("""
    SELECT
        SUM(`reserved_qty`) as reserved_qty
    FROM 
        `tabStock Reservation Entry`
    WHERE
        (`status` = 'Partially Reserved' OR `status` = 'Reserved' OR `status` = 'Partially Delivered') 
        AND `item_code` = %s 
        AND `warehouse` = %s
    """, (item_code, warehouse), as_dict=1)
    qty_reserved = item_reserved[0]['reserved_qty']


    item_delivered = frappe.db.sql("""
    SELECT
        SUM(`delivered_qty`) as delivered_qty
    FROM 
        `tabStock Reservation Entry`
    WHERE
        (`status` = 'Delivered') 
        AND `item_code` = %s 
        AND `warehouse` = %s
    """, (item_code, warehouse), as_dict=1)
    qty_delivered = item_delivered[0]['delivered_qty']

    actual_qty = qty_reserved - qty_delivered

    bin_qty = frappe.db.get_value("Bin" , filters={"item_code":item_code, "warehouse":warehouse} , fieldname = 'actual_qty')
    total = bin_qty - actual_qty
    return total
