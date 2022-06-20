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



@frappe.whitelist()
def submit_journal_entry (doc,fun=''):
    if "Cheques" in DOMAINS :
        submit_journal_entry_cheques(doc)
    



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
    #series = "Tax-Inv-.DD.-.MM.-.YYYY.-.###." if getattr(self,'tax_auth' , 0) else self.naming_series
    self.name = self.item_name