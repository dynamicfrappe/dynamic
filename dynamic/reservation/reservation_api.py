


import frappe
from frappe import _
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability

DOMAINS = frappe.get_active_domains()


def stock_ledger_entry_before_insert(stock_leger_entry_doc,*args,**kwargs):
    if 'Reservation' in DOMAINS:
        item_code = stock_leger_entry_doc.get('item_code')
        warehouse = stock_leger_entry_doc.get('warehouse')
        out_qty = abs(stock_leger_entry_doc.get('actual_qty'))
        voucher_type = stock_leger_entry_doc.get('voucher_type')
        voucher_no = stock_leger_entry_doc.get('voucher_no')
        if voucher_type=="Delivery Note" or voucher_type=='Sales Invoice':
            # get_avail_bin_qty(item_code,warehouse,out_qty)
            check_voucher_type(voucher_type,voucher_no,item_code,warehouse)
    if 'Real State' in DOMAINS:
        if stock_leger_entry_doc.actual_qty > 0:
            item_code = stock_leger_entry_doc.get('item_code')
            warehouse = stock_leger_entry_doc.get('warehouse')
            get_avail_bin_qty(item_code,warehouse,stock_leger_entry_doc.actual_qty)

def check_voucher_type(voucher_type,voucher_no,item_code,warehouse):
    if voucher_type == "Delivery Note":
        delivery_note_doc = frappe.get_doc("Delivery Note",voucher_no )
        '''
        1-get against doctype to delivery note 
        2-get against(sales_order) items inner join delivery note items 
        3-if reservation : update qty
        '''
        if len(delivery_note_doc.items):
            against_sales_order, against_sales_invoice = frappe.db.get_value('Delivery Note Item',{'parent':voucher_no},['against_sales_order', 'against_sales_invoice'])
            if against_sales_order:
                get_item_sales_order(voucher_no,against_sales_order,item_code,warehouse,join_table='tabDelivery Note Item')
            elif against_sales_invoice:
                against_sales_order = frappe.db.get_value('Sales Invoice Item',{'parent':against_sales_invoice},'sales_order')
                get_item_sales_order(voucher_no,against_sales_order,item_code,warehouse,join_table='tabDelivery Note Item')
    if voucher_type == "Sales Invoice":
        against_sales_order = frappe.db.get_value('Sales Invoice Item',{'parent':voucher_no},'sales_order')
        get_item_sales_order(voucher_no,against_sales_order,item_code,warehouse,join_table='tabSales Invoice Item')


def get_item_sales_order(delivery_name,so_name,item_code,warehouse,join_table):
    reservation_check = frappe.db.get_value('Sales Order',so_name,'reservation_check')
    if reservation_check:
        sql_items = f"""
        SELECT `tabSales Order Item`.item_code,`tabSales Order Item`.warehouse, `{join_table}`.qty
        , `tabSales Order Item`.reservation
        ,`tabSales Order Item`.parent
        FROM `tabSales Order Item` 
        INNER JOIN `{join_table}`
        ON `{join_table}`.item_code=`tabSales Order Item`.item_code
        AND `{join_table}`.warehouse=`tabSales Order Item`.warehouse
        WHERE `tabSales Order Item`.parent='{so_name}' AND `{join_table}`.parent='{delivery_name}'
        AND `tabSales Order Item`.item_code='{item_code}' AND `tabSales Order Item`.warehouse='{warehouse}'
        """
        sql_items_data = frappe.db.sql(sql_items,as_dict=1)
        update_reservation_qty(sql_items_data)

def update_reservation_qty(reserv_date):
    for row in reserv_date:
        sql_update = f"""
            Update `tabReservation Warehouse` 
            INNER JOIN `tabReservation`
            ON `tabReservation`.name=`tabReservation Warehouse` .parent
            SET `tabReservation Warehouse`.reserved_qty=(`tabReservation Warehouse`.reserved_qty-{row.qty}) 
            ,`tabReservation`.status=IF((`tabReservation Warehouse`.reserved_qty-{row.qty}=0),'Closed','Partial Delivered')
            WHERE `tabReservation Warehouse`.warehouse='{row.warehouse}' AND `tabReservation Warehouse`.item='{row.item_code}'
            AND `tabReservation`.name='{row.reservation}'

        """
        frappe.db.sql(sql_update)


def get_avail_bin_qty(item_code,warehouse,in_qty):
    actual_qty = (get_stock_availability(item_code,warehouse)[0] or 0)
    if actual_qty + in_qty  > 1:
        frappe.throw(_(f"Item Has QTY : {actual_qty} Cant't Be More Than 1 ."))
       
# # for sales order --> get avail qty - reserved qty
# def validate_avail_qty(voucher_type,voucher_no,item_code,warehouse,out_qty):
#     '''
#         1-check is there is  avail stock to get out items from stock
#     '''
#     sql=f"""
#                 SELECT `tabBin`.name as bin , 'Bin' as `doctype`,
# 				CASE 
# 						WHEN `tabReservation Warehouse`.reserved_qty > 0
# 						then `tabBin`.actual_qty - SUM(`tabReservation Warehouse`.reserved_qty)
# 						ELSE `tabBin`.actual_qty 
# 						END  as avail_qty
# 				FROM 
# 				`tabBin`
# 				LEFT JOIN 
# 				`tabReservation Warehouse`
# 				ON `tabBin`.name = `tabReservation Warehouse`.bin 
# 				LEFT JOIN 
# 				`tabReservation` 
# 				ON `tabReservation Warehouse`.parent = `tabReservation`.name 
# 				AND `tabBin`.name = `tabReservation Warehouse`.bin
# 				WHERE `tabBin`.warehouse = '{warehouse}'
# 				AND `tabBin`.item_code = '{item_code}'
# 				AND `tabReservation`.status <> "Invalid"		
#     """
#     query_data = frappe.db.sql(sql,as_dict=1)[0] or 0
#     print('\n\n\n\n\n===validate_avail_qty=>',query_data)
#     if out_qty > query_data.avail_qty:
#         frappe.throw(_("Not Avail QTY"))
    