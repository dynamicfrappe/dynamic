from datetime import datetime
import frappe
from frappe import _
from dynamic.gebco.doctype.sales_invocie.stock_settings import caculate_shortage_item
DOMAINS = frappe.get_active_domains()
import datetime

def validate_sales_invoice(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        if doc.maintenance_template:
            m_temp = frappe.get_doc("Maintenance Template",doc.maintenance_template)
            m_temp.sales_invoice = doc.name
            m_temp.save()
        if doc.maintenance_contract:
            contract_doc = frappe.get_doc("Maintenance Contract",doc.maintenance_contract)
            contract_doc.sales_invoice = doc.name
            contract_doc.save()
        #validate stock amount in packed list 
        #send  packed_items to valid and get Response message with item and shrotage amount and whare house  
        # this fuction validate current srock without looking for other resources    
        # if len(doc.packed_items) > 0  and doc.update_stock == 1:
        #     caculate_shortage_item(doc.packed_items ,doc.set_warehouse)
def validate_delivery_note(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        if doc.maintenance_template:
            m_temp = frappe.get_doc("Maintenance Template",doc.maintenance_template)
            m_temp.delivery_note = doc.name
            m_temp.save()
        if len(doc.packed_items) > 0  :
            caculate_shortage_item(doc.packed_items ,doc.set_warehouse)
    if 'Terra' in DOMAINS:
        # frappe.throw('Validate delivery Note')
        minus_delivery_qty_from_reservation(doc,*args,**kwargs)


def minus_delivery_qty_from_reservation(doc,*args,**kwargs):
    #1-qty deliverd from delivery note
    for row in doc.items:
        reserv_data = frappe.db.get_value('Sales Order Item',{'item_code':row.item_code,'parent':row.against_sales_order},['reservation','item_purchase_order','item_warehouse'],as_dict=1)
        reserv_doc = frappe.get_doc('Reservation',reserv_data['reservation'])
        #2- get row from & get reservation then check it reserver over warehouse or po -> then minus qty from reservation
        if reserv_data.get('item_purchase_order'):
            item = frappe.get_doc('Reservation Purchase Order',reserv_doc.reservation_purchase_order[0].name)
        if reserv_data.get('item_warehouse'):
            item = frappe.get_doc('Reservation Warehouse',reserv_doc.warehouse[0].name)
        if(item.reserved_qty < row.qty):
            frappe.throw(f'Not Enough Reservation qty for item {row.item_code} for reservation {reserv_data["reservation"]} avail reserved qty {item.reserved_qty}')
        item.reserved_qty = item.reserved_qty - row.qty
        item.save() 

    

def validate_purchase_recipt(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        for item in doc.items:
            serial_list = str(item.serial_no).splitlines()
            if item.serial_no:
                if item.serial2:
                    s2_list = item.serial2.splitlines()
                    if len(serial_list) == len(s2_list):
                        for i in range(0,len(serial_list)):
                            sql= """select name from `tabSerial No` where serial2='%s'"""%s2_list[i]
                            res = frappe.db.sql(sql,as_dict=1)
                            if len(res) > 0:
                                frappe.throw(_(f"Serial No {s2_list[i]} Already Exist"))
                            serial_doc = frappe.get_doc("Serial No",serial_list[i])
                            serial_doc.serial2 = s2_list[i]
                            serial_doc.save()
                    else:
                        frappe.throw(_("Serial No list Doest Not Equal Serial2"))


@frappe.whitelist()
def create_installation_request(sales_order):
    sales_order_doc = frappe.get_doc('Sales Order',sales_order)
    installation_request_doc = frappe.new_doc("Installation Request")
    installation_request_doc.sales_order = sales_order
    installation_request_doc.customer = sales_order_doc.customer
    installation_request_doc.customer_name = sales_order_doc.customer_name
    installation_request_doc.total_cars = sales_order_doc.not_requested_cars
    installation_request_doc.posting_date = datetime.datetime.now()
    installation_request_doc.save()
    return installation_request_doc
    