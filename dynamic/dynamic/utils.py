import frappe 
from erpnext.accounts.utils import get_account_currency, get_balance_on
from frappe.utils import today

#dynamic.dynamic.utils



def create_customizations(*args , **kwargs) :
   """ 
      this run on migrate to create custom field in payment entry to avoid any crash 

      """
   # add exchange rate to payment entry
   create_currency_exchange()
   # add field to journal entry account fuction 
   create_currency_exchange_je()


# Create Field Exchange rate to journal entry account 
def create_currency_exchange_je(*args,**kwargs) :
   old_fields = frappe.db.sql(""" 
         SELECT name FROM `tabCustom Field` WHERE 
         dt = "Journal Entry Account" AND fieldname = "account_currency_exchange"
   """ ,as_dict=1) 
   if old_fields and len(old_fields) > 0 :
      print("currency_exchange Filed is exit")
      return 0
   field = frappe.new_doc("Custom Field")
   field.dt = "Journal Entry Account"
   field.label = "Account Currency Exchange"
   field.fieldname = "account_currency_exchange"
   field.insert_after  ="balance"
   field.read_only = 1
   #field.hidden = 1
   field.fieldtype = "Data"
   field.save()
   print("currency_exchange Filed is created")
#Create Field in payment entry to currency exchange rate
def create_currency_exchange(*args , **kwargs) :
   # chek if field exit
   old_fields = frappe.db.sql(""" 
   SELECT name FROM `tabCustom Field` WHERE 
   dt = "Payment Entry" AND fieldname = "currency_exchange"
   """ ,as_dict=1) 
   if old_fields and len(old_fields) > 0 :
      print("currency_exchange Filed is exit")
      return 0
   field = frappe.new_doc("Custom Field")
   field.dt = "Payment Entry"
   field.label = "Currency Exchange"
   field.fieldname = "currency_exchange"
   field.insert_after  ="paid_from_account_balance"
   field.read_only = 1
   field.hidden = 1
   field.fieldtype = "Data"
   field.save()
   print("currency_exchange Filed is created")

@frappe.whitelist()
def currency_valuation_rate(account ) :
   date = today()
   balance_in_compnay_currency = get_balance_on (account =account ,date =str(date))
   balance_in_account_currency = get_balance_on (account =account ,date =str(date) , in_account_currency=False)
   try :
      valuation =  balance_in_account_currency / balance_in_compnay_currency
      return valuation 
   except Exception as e :
      print("-----------------------------------",str(e))
      return False


