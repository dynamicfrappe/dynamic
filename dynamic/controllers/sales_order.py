



import frappe
from frappe import _
from frappe import _, bold
from dynamic.qaswaa.controllers.sales_order_api import validate_item_qty_reserved
from dynamic.terra.api import sales_order_submit_comlete_opportunity
Domains=frappe.get_active_domains()

def validate_sales_order(self , event):
    if "Qaswaa" in Domains :
        validate_item_qty_reserved(self,event)
    if "Healthy Corner" in Domains :
        item_discount_rate(self)

def validate_sales_order_for_stock(self , event):
    if "Stock Reservation" in Domains:
        get_validation(self,event)

    
        if frappe.db.get_single_value("Stock Settings" , "auto_reserve_stock_in_warehouse"):
            reserve_in_warehouse(self , event)

def on_submit(self , event):
    if "Stock Reservation" in Domains:
        if frappe.db.get_single_value("Stock Settings" , "allow_partial_reservation"):
            if self.reserve_stock:
                creation_of_reseration(self , event)
        if frappe.db.get_single_value("Stock Settings" , "auto_reserve_stock_in_warehouse"):
                transfer_items(self , event)
    if "Terra"  in Domains : 
        sales_order_submit_comlete_opportunity(self)
def on_update(self , event):
    if "Stock Reservation" in Domains:
        # if frappe.db.get_single_value("Stock Settings" , "allow_partial_reservation"):
        if self.reserve_stock:
            creation_of_reseration(self , event)
        
def on_cancel(self , event):
    if "Stock Reservation" in Domains:
        cencel_reservation(self , event)
        

def cencel_reservation(self , event):
    items = self.get("items")
    for item in items:
        doc = frappe.get_doc("Stock Reservation Entry" , {
            "item_code":item.item_code,
            "warehouse":item.warehouse,
            "voucher_no":self.name ,
            "voucher_detail_no" : item.name
            })
        doc.status = "Cancelled" 
        doc.save(ignore_permissions=True)


def item_discount_rate(self):
    item_discount_rate = self.discount_item or 0
    for item in self.items:
        item.discount_percentage = item_discount_rate
        if item_discount_rate is not None:
            item.discount_amount = item.price_list_rate * (item_discount_rate / 100)
        else:
            item.discount_amount = 0  
        item.rate = item.price_list_rate - item.discount_amount
        item.amount = item.rate * item.qty

def transfer_items(self , *args, **kwargs):
    items = self.get("items")
    stock_entry_type = frappe.db.get_value("Stock Entry Type" , filters={"purpose":"Material Transfer"} , fieldname = 'name')
    stock_adjustment_account = frappe.db.get_value("Company" , self.company , fieldname = 'stock_adjustment_account')

    doc = frappe.new_doc("Stock Entry")
    doc.stock_entry_type = stock_entry_type
    doc.from_warehouse = self.reserve_for_warehouse
    doc.to_warehouse = self.set_warehouse
    for item in items:
        doc.append("items", {
        "s_warehouse": doc.from_warehouse,
        "t_warehouse": doc.to_warehouse,
        "item_code": item.item_code,
        "qty":item.qty_to_reserve , 
        "uom": item.uom , 
        "conversion_factor" : item.conversion_factor , 
        "ref_sales_order" : self.name , 
        "ref_idx": item.name ,
        "cost_center": self.cost_center,
        "expense_account": stock_adjustment_account
    })
    doc.submit()
    # doc.insert()        

    
def reserve_in_warehouse(self, *args, **kwargs):
    warehouse = frappe.db.get_single_value("Stock Settings" , "warehouse")
    if warehouse:
        self.reserve_for_warehouse = warehouse
        items = self.get("items")
        for item in items:
            item.warehouse = warehouse


def creation_of_reseration(self , *args , **kargs):
    items = self.get("items")
    for item in items:
        if frappe.db.exists("Stock Reservation Entry" ,{
				"item_code": item.item_code,
				"warehouse": item.warehouse,
				"voucher_no": self.name,
				"voucher_detail_no" : item.name
				}):
            frappe.msgprint("Create Reservation Before")
        else:
            log = frappe.new_doc("Stock Reservation Entry")
            log.item_code = item.item_code
            log.warehouse = item.warehouse
            log.voucher_type = "Sales Order"
            log.voucher_no = self.name
            log.voucher_detail_no = item.name
            log.stock_uom = item.uom
            log.available_qty_to_reserve = get_all_qty_reserved(item.item_code , item.warehouse)
            log.reserved_qty = float(item.qty_to_reserve) * float(item.conversion_factor)
            log.voucher_qty = item.qty_to_reserve 
            log.company = self.company
            log.status = "Reserved"
            frappe.msgprint("Item Reservation")
            log.insert(ignore_permissions=True)
            frappe.db.commit()
                

def convertor( item_code , uom ):
    item = frappe.get_doc("Item" , item_code)
    conversion_factor = 1
    uoms = item.get("uoms")
    for i in uoms:
        if uom == i.uom:
            conversion_factor = i.conversion_factor
    return conversion_factor


def get_validation(self , *args, **kwargs):
    if frappe.db.get_single_value("Stock Settings" , "allow_partial_reservation"):
        if not self.reserve_stock:
            return True
        items = self.get("items")
        for item in items:
            item_code = item.item_code
            qty = float(item.qty_to_reserve or 0)
            warehouse = item.warehouse
            total_qty = get_all_qty_reserved (item_code, warehouse)
            if qty > total_qty:
                wanted_qty = float(qty) - float(total_qty)
                msg = f"""
                    Item Name {bold(item.item_code)} Need Qty {bold(wanted_qty)}<br>
                    """
                frappe.throw(msg)




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
        (`status` = 'Partially Reserved' OR `status` = 'Reserved' OR `status` = 'Partially Delivered') 
        AND `item_code` = %s 
        AND `warehouse` = %s
    """, (item_code, warehouse), as_dict=1)
    qty_delivered = item_delivered[0]['delivered_qty']

    actual_qty = float(qty_reserved or 0 ) - float( qty_delivered or 0 )
    bin_qty = frappe.db.get_value("Bin" , filters={"item_code":item_code, "warehouse":warehouse} , fieldname = 'actual_qty')
    total = float(bin_qty or 0) - float(actual_qty or 0)
    return total
