from datetime import datetime
from dynamic.dynamic_accounts.print_format.invoice_tax.invoice_tax import get_invoice_tax_data
import frappe 
from frappe import _
import codecs
import json
import base64
from .product_bundle.doctype.packed_item.packed_item import  make_packing_list
from erpnext import get_default_company, get_default_cost_center
from frappe.model.naming import make_autoname
from frappe.utils.user import get_users_with_role
from frappe.utils.background_jobs import enqueue
from dynamic.product_bundle.doctype.packed_item.packed_item import make_packing_list
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
from dynamic.dynamic.validation import validate_sales_invoice
from dynamic.gebco.doctype.sales_invocie.stock_settings import caculate_shortage_item
DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def validate_active_domains(doc,*args,**kwargs):
    if  'Moyate' in DOMAINS: 
        """   Validate Sales Commition With Moyate """
        validate_sales_invocie_to_moyate(doc)


    if 'Product Bundle' in DOMAINS: 
        """   Update Bundle of Bundles """
        make_packing_list(doc)

    
    if 'Terra' in DOMAINS:
        validate_sales_invoice(doc)

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
            caculate_shortage_item(doc.packed_items ,doc.set_warehouse)

@frappe.whitelist()
def submit_journal_entry (doc,fun=''):
    if "Cheques" in DOMAINS :
        submit_journal_entry_cheques(doc)
    

@frappe.whitelist()
def validate_devliery_note(doc , *args, **kwargs):
    pass

@frappe.whitelist()
def submit_journal_entry_cheques (doc):
    if getattr(doc,"payment_entry",None):
        payment_entry = frappe.get_doc("Payment Entry",doc.payment_entry)
        payment_entry.cheque_status = doc.cheque_status
        payment_entry.save()



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
        self.name = self.item_name


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




def check_email_setting_in_stock_setting(doc):
    sql = """
    select document,role from `tabEmail Setting`;
    """
    setting_table = frappe.db.sql(sql,as_dict=1)
    if setting_table:
        for row in setting_table:
            if row.document == "Purchase Recipt" and row.role:
                link_str = frappe.utils.get_url_to_form("Purchase Recipt",doc.name)
                msg = f"New Purchase Recipt Created  {link_str}"
                send_mail_by_role(row.role,msg,"Purchase Recipt")
            # if row.document == "Item Re Order" and row.role:
            #     msg = f"New Purchase Recipt Created  {link_str}" 
            # if row.document == "Safty Stock" and row.role:
            #     pass



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
        




# @frappe.whitelist()
def send_mail_by_role(role,msg,subject):
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


def validate_sales_order_items_amount(self,*args , **kwargs):
    frappe.errprint(f'data self-->{self}')
    #check item in purchase order
    #check item in stock
    pass