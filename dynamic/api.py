from datetime import datetime
from warnings import filters
from dynamic.dynamic_accounts.print_format.invoice_tax.invoice_tax import get_invoice_tax_data
import frappe 
from frappe import _
import codecs
import json
import erpnext
import base64
#from .product_bundle.doctype.packed_item.packed_item import  make_packing_list
from dynamic.product_bundle.doctype.packed_item.new_packed_item import make_packing_list
from erpnext import get_default_company, get_default_cost_center
from frappe.model.naming import make_autoname
from frappe.utils.user import get_users_with_role
from frappe.utils.background_jobs import enqueue
#from dynamic.product_bundle.doctype.packed_item.packed_item import make_packing_list
from frappe.utils import add_days, nowdate, today
from dynamic.cheques.doctype.cheque.cheque import add_row_cheque_tracks
from dynamic.terra.delivery_note import validate_delivery_notes_sal_ord
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import repost_entries
from dynamic.gebco.doctype.sales_invocie.utils import set_complicated_pundel_list
from datetime import date
@frappe.whitelist()
def encode_invoice_data(doc):
    doc = frappe.get_doc("Sales Invoice",doc)
    company = frappe.get_doc("Company",doc.company)
    invoice_data = get_invoice_tax_data(doc.name) or {}
    # print('doc => ' ,doc)
    data_dict = [
        {
            "tagNumber" : 1 ,
            "value" : str(company.company_name or "") 
        },
        {
            "tagNumber" : 2 ,
            "value" : str(company.tax_id or "") 
        },
        {
            "tagNumber" : 3 ,
            "value" : str (doc.posting_date) + " " + str(doc.posting_time) 
        },
        {
            "tagNumber" : 4 ,
            "value" : str((doc.base_rounded_total or doc.base_grand_total )or "") 
        },
        {
            "tagNumber" : 5 ,
            "value" : str(invoice_data.get("total_tax_amount") or "") 
        },
    ]
    total_hex = ""
    for row in data_dict :
        value = row["value"].encode("utf-8").hex()
        if len(row["value"]) > 15:
            value_len = hex(len(row["value"])).replace('0x','')
        else :
            value_len = hex(len(row["value"])).replace('x','')
        tagNumber = hex(row['tagNumber']).replace('x','')

        # value_len = hex(len(row["value"])).replace('0x','')
        # tagNumber = hex(count).replace('0x','')

        total_hex_str = str(tagNumber + value_len+value)

        # hexa_tag = total_hex_str.encode("utf-8")
        total_hex += total_hex_str
        print ("**********************************************")
        print (row["value"])
        print ("value => " , value)
        print ("value_len => " , value_len)
        print ("tagNumber => " , tagNumber)
        print ("total_hex_str => ", total_hex_str)
        # print ("hexa_tag => ", hexa_tag)
    total_hex_b64 = codecs.encode(codecs.decode(total_hex, 'hex'), 'base64').decode('utf-8')
    return total_hex_b64

import frappe
from frappe import _
from .api_hooks.sales_invoice import validate_sales_invocie_to_moyate
from dynamic.dynamic.validation import get_active_domain, validate_sales_invoice
from dynamic.gebco.doctype.sales_invocie.stock_settings import caculate_shortage_item
from dynamic.gebco.doctype.stock_ledger import get_valuation_rate

DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def validate_active_domains(doc,*args,**kwargs):
    if  'Moyate' in DOMAINS: 
        """   Validate Sales Commition With Moyate """
        validate_sales_invocie_to_moyate(doc)


    if 'Product Bundle' in DOMAINS: 
        """   Update Bundle of Bundles """
        make_packing_list(doc)
        # add child table to sales invoice from utils 

        set_complicated_pundel_list(doc)
    
    if 'Terra' in DOMAINS:
        #validate_sales_invoice(doc)
        pass
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
        if len(doc.packed_items) > 0  and doc.update_stock == 1:
            caculate_shortage_item(doc.packed_items + doc.items  ,doc.set_warehouse)   
    if 'IFI' in DOMAINS:
        # check sINV items valutaion rate
        check_item_valuation_rate(doc)

def check_item_valuation_rate(doc):
    for item in doc.items:
        value_rate = get_valuation_rate(item.item_code,
        item.warehouse,
        item.parenttype,
        item.parent,
        allow_zero_rate=False,
        currency=erpnext.get_company_currency(doc.company),
        company=doc.company,
        raise_error_if_no_rate=True,
        )
        if(value_rate):
            if(item.rate < value_rate):
                frappe.throw(_("Selling Rate cann't Be Less Than Value Rate "))

@frappe.whitelist()
def validate_active_domains_invocie(doc,*args,**kwargs):
    cur_doc  = frappe.get_doc("Sales Invoice" , doc)
    if len(cur_doc.packed_items) > 0  and cur_doc.update_stock == 1:
            caculate_shortage_item(cur_doc.packed_items + cur_doc.items ,cur_doc.set_warehouse)
@frappe.whitelist()
def validate_active_domains_note(doc,*args,**kwargs):
    cur_doc  = frappe.get_doc("Delivery Note" , doc)
   
    if len(cur_doc.packed_items) > 0 :
            caculate_shortage_item(cur_doc.packed_items + cur_doc.items ,cur_doc.set_warehouse)
@frappe.whitelist()
def submit_journal_entry (doc,fun=''):
    if "Cheques" in DOMAINS :
        submit_journal_entry_cheques(doc)

@frappe.whitelist()       
def validate_delivery_note(doc,*args,**kwargs):
    if 'Product Bundle' in DOMAINS: 
        """   Update Bundle of Bundles """
        make_packing_list(doc)
    if 'Gebco' in DOMAINS:
        if doc.maintenance_template:
            m_temp = frappe.get_doc("Maintenance Template",doc.maintenance_template)
            m_temp.delivery_note = doc.name
            m_temp.save()
        if len(doc.packed_items) > 0  :
            make_packing_list(doc)
            set_complicated_pundel_list(doc)
            caculate_shortage_item(doc.packed_items ,doc.set_warehouse)    
    if 'Terra' in DOMAINS:
        # frappe.throw('Validate delivery Note')
        validate_delivery_notes_sal_ord(doc)
        

@frappe.whitelist()       
def cancel_delivery_note(doc,*args,**kwargs):
    #1-qty deliverd from delivery note
    if  'Terra' in DOMAINS:
        for row in doc.items:
            reserv_data = frappe.db.get_value('Sales Order Item',{'item_code':row.item_code,'parent':row.against_sales_order},['reservation'],as_dict=1)
            reserv_doc = frappe.get_doc('Reservation',reserv_data['reservation'])
            reserv_doc.db_set('status','Invalid')
    

@frappe.whitelist()
def submit_journal_entry_cheques (doc):
    if getattr(doc,"payment_entry",None):
        payment_entry = frappe.get_doc("Payment Entry",doc.payment_entry)
        old_status = payment_entry.cheque_status
        payment_entry.cheque_status = doc.cheque_status
        payment_entry.save()
        add_row_cheque_tracks(doc.payment_entry,doc.cheque_status,old_status)

@frappe.whitelist()
def submit_purchase_invoice(doc , *args , **kwargs) :
    if 'Gebco' in DOMAINS:
          if doc._action == "submit":
            repost_entries()
    if 'Terra' in DOMAINS:
        check_pr_reservation(doc)

    
    #erpnext.stock.doctype.repost_item_valuation.repost_item_valuation.repost_entries
# ---------------- get sales return account ------------------  #
@frappe.whitelist()
def get_sales_return_account():
    company_name = get_default_company()
    company_doc = frappe.get_doc("Company",company_name)
    if company_doc.get("sales_return_account"):
        return company_doc.get("sales_return_account")
    return



# item auto name
def autoname(self,fun=''):
    if 'Terra' in DOMAINS:
        #series = "Tax-Inv-.DD.-.MM.-.YYYY.-.###." if getattr(self,'tax_auth' , 0) else self.naming_series
        self.name = self.item_code


@frappe.whitelist()
def generate_item_code(item_group):
    group_doc = frappe.get_doc("Item Group",item_group)
    group_code = group_doc.code
    if not group_code:
        frappe.msgprint(_("Item Group Doesnt Have Code"))
        return 'false'
    sql = f"""
    select count(*) +1 as 'serial' from `tabitem code serial` where item_group= '{group_doc.name}'
    """
    res = frappe.db.sql(sql,as_dict=1)

    serial = str(group_code or '')+'-' + str(res[0].serial or '')

    return serial


@frappe.whitelist()
def create_new_appointment(source_name, target_doc=None):
    doc = frappe.get_doc("Lead", source_name)
    appointment_doc = frappe.new_doc("Appointment")
    appointment_doc.customer_name = doc.lead_name
    appointment_doc.customer_phone_number = doc.phone_no 
    appointment_doc.appointment_with = "Lead"
    appointment_doc.party = doc.name
    appointment_doc.customer_email = doc.email_id
    return appointment_doc


from dynamic.gebco.api import validate_purchase_recipt
def submit_purchase_recipt_based_on_active_domains(doc,*args,**kwargs):
    if 'Gebco' in DOMAINS:
        validate_purchase_recipt(doc)
    if 'Terra' in DOMAINS:
        check_email_setting_in_stock_setting(doc)
        #check if PR has Reservation & reserve over warehouse
        check_pr_reservation(doc)

def check_email_setting_in_stock_setting(doc):
    sql = """
    select document,role from `tabEmail Setting`;
    """
    setting_table = frappe.db.sql(sql,as_dict=1)
    if setting_table:
        for row in setting_table:
            if row.document == "Purchase Recipt" and row.role:
                link_str = frappe.utils.get_url_to_form("Purchase Receipt",doc.name)
                msg = f"New Purchase Recipt Created  {link_str}"
                send_mail_by_role(row.role,msg,"Purchase Receipt")
            # if row.document == "Item Re Order" and row.role:
            #     msg = f"New Purchase Recipt Created  {link_str}" 
            # if row.document == "Safty Stock" and row.role:
            #     pass

def check_pr_reservation(doc):
    if doc.doctype == "Purchase Invoice":
        if  doc.update_stock:
            loop_over_doc_items(doc)
    if doc.doctype == 'Purchase Receipt':
        loop_over_doc_items(doc)

def loop_over_doc_items(doc):
    for row in doc.items:
        if(row.purchase_order):
            #get all reservation for this purchase_order wiz this item
            get_po_reservation(row.purchase_order,row.item_code,row.warehouse)

def get_po_reservation(purchase_order,item,target_warehouse):
    reservation_list_sql = f"""SELECT r.name from `tabReservation` as r WHERE r.status <> 'Invalid' AND r.order_source='{purchase_order}' AND r.item_code = '{item}' AND sales_order <> 'Invalid' AND r.warehouse_source = '' """
    data = frappe.db.sql(reservation_list_sql,as_dict=1)
    if data:
        for reservation in data:
            # make reserv over warehouse
            reserv_doc = frappe.get_doc('Reservation',reservation.get('name'))
            oldest_reservation = reserv_doc.reservation_purchase_order[0]
            bin_data = frappe.db.get_value('Bin',{'item_code':item,'warehouse':target_warehouse},['name','warehouse','actual_qty','reserved_qty'],as_dict=1)
            reserv_doc.warehouse_source = target_warehouse
            reserv_doc.warehouse = [] #?add row
            row = reserv_doc.append('warehouse', {})
            row.item = item
            row.bin = bin_data.get('name')
            row.warehouse = target_warehouse
            row.qty = oldest_reservation.qty
            row.reserved_qty =  oldest_reservation.reserved_qty
            #! not clear TODO
            row.current_available_qty = bin_data.get('actual_qty') + row.qty - bin_data.get('reserved_qty')
            # row.available_qty_atfer___reservation = bin_data.get('actual_qty') - bin_data.get('reserved_qty')#row.current_available_qty - row.reserved_qty
            reserv_doc.reservation_purchase_order = []
            reserv_doc.save()
            

def validate_material_request(doc,*args,**kwargs):
    sql = """
    select document,role from `tabEmail Setting` where document='Item Re Order';
    """
    setting_table = frappe.db.sql(sql,as_dict=1)
    if len(setting_table) > 0:
        if setting_table[0].role:
            link_str = frappe.utils.get_url_to_form("Material Request",doc.name)
            msg = f" Material Request {link_str} Created Successfully "
            send_mail_by_role(setting_table[0].role,msg,"Item Re Order")
        

def validate_material_request_cost_center(doc,*args,**Kwargs):
    if doc.get("cost_center"):
        for item in doc.get("items"):
            if not item.get("cost_center"):
                item.cost_center = doc.get("cost_center")

def onsave_material_request(doc,*args,**kwargs):
     if "Terra" in DOMAINS:
        validate_material_request_cost_center(doc)
        
import os
# @frappe.whitelist()
def saftey_stock():
    sql = """
    select document,role from `tabEmail Setting` where document='Safty Stock';
    """
    setting_table = frappe.db.sql(sql,as_dict=1)
    if len(setting_table) > 0:
        item_sql = """
            select tb.item_code  ,sum(tb.actual_qty) as 'actual_qty',ti.safety_stock 
            from tabBin tb
            inner join tabItem ti 
            on tb.item_code = ti.name
            group by tb.item_code
            HAVING  sum(tb.actual_qty) > ti.safety_stock 
        """ 
        
        item_list = frappe.db.sql(item_sql,as_dict=1)
        str_list = "This Items Exceed safty stock limit"
        str_list += "("
        for itm in item_list:
            print("aaaaaa",itm.item_code)
            str_list +=" %s , "%itm.item_code
        str_list += ")"
        print("str list",str_list)
        #shotage_string = " This Items Exceed safty stock limit " + lst_str
        
        asd = send_mail_by_role(setting_table[0].role,str_list,"Saftey Stock")
        return asd
        
@frappe.whitelist()
def check_delivery_warehosue(doc_name,item_code,warehouse):
     if not warehouse and item_code:
                purchase_warehouse_list=frappe.db.get_list('Purchase Order Item', filters={
                                    'parent':doc_name,
                                    'item_code':item_code
                                },
                                fields=['warehouse']
                                )
                return purchase_warehouse_list[0].get('warehouse')



# @frappe.whitelist()
def send_mail_by_role(role,msg,subject):
    try:
        recip_list = get_users_with_role(role)
        email_args = {
            "recipients": recip_list,
            "sender": None,
            "subject": subject,
            "message":msg,
            "now": True
        }
        print(" emails =====> ", email_args )

        if not frappe.flags.in_test:
            frappe.enqueue(method=frappe.sendmail, queue="short", timeout=500, is_async=True, **email_args)
        else:
            frappe.sendmail(**email_args)
        return email_args
    except Exception as ex:
        print("exception",str(ex))





@frappe.whitelist()
def check_source_item(self,*args , **kwargs):
    if "Terra" in DOMAINS:
        # sales_order_doc = frappe.get_doc('Sales Order',self)
        for item in self.items:
             #TODO if item has purchase and warehouse show error or both has value
            if (not item.item_warehouse and  not item.item_purchase_order):
                frappe.throw(_(f"Please Select Source As Warehouse Or Purchase Order for Item {item.item_code}"))
            if ( item.item_warehouse and  item.item_purchase_order):
                frappe.throw(_(f"Please Select Just One Source As Warehouse Or Purchase Order for Item {item.item_code} Not Both"))
            if (not item.warehouse and item.item_purchase_order):
                def_warhouse = check_delivery_warehosue(item.item_purchase_order,item.item_code,'')
                item.db_set('warehouse',def_warhouse)

    

@frappe.whitelist()
def create_reservation_validate(self,*args , **kwargs):
    if "Terra" in DOMAINS:
        add_row_for_reservation(self)
       
def add_row_for_reservation(self):
    # if not self.reservation:
    for item in self.items:
        if not item.reservation:
            reserv_doc = frappe.new_doc('Reservation')
            reserv_doc.item_code = item.item_code
            reserv_doc.status = 'Active'
            reserv_doc.valid_from = self.transaction_date
            reserv_doc.reservation_amount = item.qty
            #source in reservation = row.source else slaes_order_source
            reserv_doc.warehouse_source = item.item_warehouse if item.item_warehouse  else "" #self.set_warehouse
            if not reserv_doc.warehouse_source:
                reserv_doc.order_source = item.item_purchase_order if item.item_purchase_order else "" #self.purchase_order
            reserv_doc.save()
            item.reservation = reserv_doc.name
            item.reservation_status = reserv_doc.status
            item.save()
            reserv_doc.db_set('sales_order',self.name)


@frappe.whitelist()
def cancel_reservation(self,*args , **kwargs):
    if "Terra" in DOMAINS:
        for item in self.items:
            if(item.reservation):
                frappe.db.set_value('Reservation',item.reservation,'status','Invalid')




@frappe.whitelist()
def validate_sales_order_reservation_status():

    # 1- get conf
    reservation_conf = """
    select * from `tabReservation Child`
    """
    conf_result = frappe.db.sql(reservation_conf,as_dict=1)

    # 2- get all sales order with reservation_status = 'Active'
    sql = """
        select 
            tso.name
            ,tsoi.name as 'childname'
            ,tsoi.reservation 
            ,tsoi.reservation_status
            ,tso.advance_paid
            ,tso.base_grand_total
            ,DATEDIFF(CURDATE(),tso.creation) as 'diff' 
            from 
            `tabSales Order Item` tsoi
            inner join `tabSales Order` tso 
            on tso.name = tsoi .parent 
            where tsoi.reservation  is not null and tsoi.reservation_status ='Active'
        """
    sales_order_result = frappe.db.sql(sql,as_dict=1)

    # loop throgth conf and update sales order that achive criteria
    for c in conf_result:
        for s in sales_order_result:
            if s.diff >= float(c.days or 0) and ((float(s.advance_paid or 0) / s.base_grand_total) *100 < float(c.percent or 0) or c.percent==0):
                #sales_order = frappe.get_doc("Sales Order",s.name)
                reserv_doc = frappe.get_doc("Reservation",s.reservation)
                reserv_doc.status = "Closed"
                reserv_doc.closing_date = nowdate()
                reserv_doc.save()
                # sales_order.reservation_status = "Closed"
                # sales_order.save()
                sql = f""" update `tabSales Order Item` set  reservation_status='Closed' where name='{s.childname}'"""
                frappe.db.sql(sql)
                frappe.db.commit()
                





@frappe.whitelist()
def get_active_domains():
    return frappe.get_active_domains()
    
@frappe.whitelist()
def submit_payment(doc,*args,**kwargs):
     if "Terra" in DOMAINS:
          submit_payment_for_terra(doc)


@frappe.whitelist()
def submit_payment_for_terra(doc , *args ,**kwargs):
    if doc.references and len (doc.references) > 0 :
        for ref in doc.references :
            if ref.reference_doctype in ["Sales Order" , "Sales Invoice" ]  :
                
                out_stand = frappe.db.sql(f"""SELECT 
                b.total_amount - SUM(b.allocated_amount)  AS out_stand FROM 
                `tabPayment Entry Reference` b
                Inner Join `tabPayment Entry` a 
                ON a.name = b.parent
                WHERE b.reference_doctype ="{ref.reference_doctype}" AND 
                b.reference_name ='{ref.reference_name}' AND a.docstatus =1
                """,as_dict =1)  
                # update sales order allocated amount if payment againest sales order 
                if ref.reference_doctype == "Sales Order" :
                    if out_stand and out_stand[0].get("out_stand") : 
                        frappe.db.sql(f""" UPDATE `tabSales Order` SET 
                        outstanding_amount ={ out_stand[0].get("out_stand")} 
                        WHERE name = "{ref.reference_name}" """)
                        frappe.db.commit()
                
                  # update sales order allocated amount if payment againest sales invoice 
                if ref.reference_doctype == "Sales Invoice" :
                    #get invoice total 
                    invoice_total = frappe.db.get_value("Sales Invoice" , ref.reference_name ,"total")
                   
                    sales_invoice = frappe.get_doc("Sales Invoice" , ref.reference_name )
                    orders =[]
                    for line  in sales_invoice.items :
                        if line.sales_order not in orders :
                            # frappe.throw(str(line.sales_order))
                            order_amount = frappe.db.sql(f"""SELECT SUM(b.amount) AS amount 
                                    FROM 
                                    `tabSales Invoice Item` b 
                                    inner join `tabSales Invoice` a 
                                    ON a.name = b.parent
                                    WHERE  
                              b.sales_order  ="{line.sales_order}" 
                              AND a.docstatus =1""",as_dict = 1)
                            orders.append(line.sales_order)
                            if len(orders) > 1 :
                                frappe.throw(""" Sales Invocie Line Have To many orders """)
                            if len(order_amount) >  0 and order_amount[0].get("amount") :
                                # oreder_perecent = float(order_amount[0].get("amount")) / float(invoice_total or 0)
                                # order_amount = line.amount * oreder_perecent
                                amount =out_stand[0].get("out_stand")
                                order_name = line.sales_order
                                frappe.db.sql(""" UPDATE `tabSales Order`  SET  outstanding_amount = %d 
                                 WHERE name = '%s'  """%(amount , order_name))
                                frappe.db.commit()


                                #frappe.throw(str(oreder_perecent))
                    



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_purchase_order(doctype, txt, searchfield, start, page_len, filters):
    if  filters and filters.get("item_code"):
        return frappe.db.sql(
            f"""select po.parent from `tabPurchase Order Item` po
                where po.item_code = '{filters.get("item_code")}' AND IFNULL(po.received_qty,0) < po.qty
                """
        )
    return ()


@frappe.whitelist()
def change_row_after_submit(doc , *args ,**kwargs):
    if('Terra' in DOMAINS):
        """
        1-get all reservation list for sales order
        2-then update qty if this reservation still exist 
        3-set status as invalid for reserv if  row deleted
        4- create new reservation if new row added
        """
        sql_reserv = f"""
            select name from tabReservation tr where sales_order ='{doc.name}'
        """
        sql_reserv = frappe.db.sql(sql_reserv)
        sql_reserv_list = [l[0] for l in sql_reserv]
        for row in doc.items:
            if(row.reservation and row.reservation_status == 'Active'):
                if(row.get('item_purchase_order')):
                    sql = f"""
                        UPDATE `tabReservation Purchase Order` trpo
                        SET trpo.reserved_qty  = {row.qty}
                        WHERE trpo.parent='{row.reservation}' AND Item='{row.item_code}';
                    """
                    frappe.db.sql(sql)
                if row.get('item_warehouse'):
                    sql = f"""
                        UPDATE `tabReservation Warehouse` trw
                        SET trw.reserved_qty  = {row.qty}
                        WHERE trw.parent='{row.reservation}' AND Item='{row.item_code}';
                    """
                    frappe.db.sql(sql)

                if row.reservation in sql_reserv_list:
                    sql_reserv_list.remove(row.reservation)
            # if(not row.reservation):
            #     #**check if have ware house or purchase invoice
            #     check_source_item(doc)
            #     #**create reservation
            #     add_row_for_reservation(doc)
        else:
            if len(sql_reserv_list):
                for reservation in sql_reserv_list:
                    frappe.db.set_value('Reservation',reservation,{'status':'Invalid'})
    


#add Whats App Message send Button 
@frappe.whitelist()
def validate_whatsApp(*args , **kwargs) :
      if  'Moyate' in DOMAINS: 
        """   Validate Sales Commition With Moyate """
        return True


@frappe.whitelist()
def validate_whats_app_settings(data , *args ,**kwargs) :
    json_data = json.loads(data)
    #get_active_profile 
    profile = frappe.db.sql(""" SELECT name from `tabWhatsApp`  WHERE status = 'Active' """ ,as_dict =1)
    if len(profile) == 0 :
        frappe.throw("No Active profile")
    if len(profile) > 0 :
        for i in json_data :
            msg = frappe.new_doc("Whats App Message")
            msg.customer = frappe.get_doc("Customer" ,i.get("name")).name
            msg.fromm = profile[-1].get("name")
            msg.save()
            # frappe.throw(i.get("name"))





# @frappe.whitelist()
def modeofpaymentautoname(self,fun=''):
    print("************************************************** ")
    #frappe.throw("----------------------------------------------")
    if "Terra" in DOMAINS:
        mode_of_payment = frappe.get_doc("Mode of Payment",self.mode_of_payment)
        if mode_of_payment.naming:
            sql = "select count(*) as 'c' from `tabPayment Entry` WHERE mode_of_payment='%s'"%self.mode_of_payment
            last_id = frappe.db.sql(sql,as_dict=1)
            todays_date = date.today()
            year = todays_date.year
            id = int(last_id[0].get("c")) +1
            if mode_of_payment.naming == "Cash-.YYYY.-":
                self.name = "Cash"+"-"+str(year)+"-" + str(id)
            elif mode_of_payment.naming == "Bank-.YYYY.-":
                self.name = "Bank"+"-"+str(year)+"-" + str(id)

            self.mode_of_payment_naming = mode_of_payment.naming

@frappe.whitelist()
def validate_mode_of_payment_naming(old_naming=None,mode_of_payment=None,*args, **kwargs):
    if not mode_of_payment or not old_naming:
        return True
    doc = frappe.get_doc("Mode of Payment",mode_of_payment)
    if doc.naming == old_naming:
        return True
    return False