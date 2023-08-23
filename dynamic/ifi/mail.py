import frappe 
import datetime 
from frappe.utils import add_to_date ,today ,getdate ,now
from frappe.email.doctype.email_queue.email_queue import send_now
def get_un_send_mails(*args , **kwargs) :
   """ 
   1- get name for all un send mails in last Tow hours 
   Not Sent
   select name ,creation  ,status FROM `tabEmail Queue` WHERE status = 'Not Sent' ; 

   """

   current_time = now() 
   end_time = add_to_date(current_time , hours=2)


   data = frappe.db.sql(f""" 
   select name ,creation  ,status FROM `tabEmail Queue` WHERE status = 'Not Sent' 
   AND  creation > date('{end_time}') ; 
   """,as_dict =1 )
 
   if data and len(data) > 0 : 
      for i in data :
         send_now(i.get("name"))

   pass