import frappe
from frappe import _
from frappe.utils import get_host_name, escape_html , today ,getdate
import json
no_cache = 1

     
main_url = "http://0.0.0.0:8002/api/method/dynamic.www.reservation.get_department_specialty"
search_url = "http://0.0.0.0:8002/api/method/dynamic.www.reservation.get_patients"


@frappe.whitelist(allow_guest=True)
def search(*args, **kwargs) :
   res = []
   data = False 
   try : 

      data = json.loads(frappe.request.data)
   except  :
      pass
   if data :
      query = data.get("search")
      if query :
         sql_srt = """ SELECT """
   return res

@frappe.whitelist(allow_guest=True)
def get_department_specialty():
   res = []
   data =  json.loads( frappe.request.data)
   if data.get('dep') :
      dep = data.get('dep')
      res=  frappe.db.sql(f""" SELECT name FROM `tabMedical Specialty` 
                              WHERE medical_department ='{dep}' """,as_dict=1)
   return res 


@frappe.whitelist(allow_guest=True)
def get_department() :
   """ 
   this function check all department with medidcat specialiest connects with 
   
   """
   department_data = frappe.db.sql(""" 
   SELECT medical_department FROM `tabMedical Specialty`  WHERE docstatus=1 
   GROUP BY medical_department
   """,as_dict=1)
   return department_data


@frappe.whitelist(allow_guest=True)
def get_patients() :
   try :
      data =  json.loads( frappe.request.data)
   except :
      data = False
   sql_str = f""" SELECT patient_name  ,name , phone , email ,sex , blood_group ,dob ,mobile
               FROM tabPatient WHERE status='Active' """
   if data :
      if data.get("search") :
         sql_str = sql_str + f"""AND patient_name like '%{data.get("search")}%' or
          phone like '%{data.get("search")}%' """
   if data :
      if data.get("name") :
         sql_str = sql_str + f"""AND patient_name = "{data.get("name")}" """  
   req = frappe.db.sql(sql_str ,as_dict=1)
   return req

      
@frappe.whitelist(allow_guest=False)
def get_context(context):
   if frappe.session.user == "Guest":
      csrf_token = False
   if frappe.session.user != "Guest":
      csrf_token = frappe.sessions.get_csrf_token()
   context.currenturl = frappe.utils.get_url()
   context.date = today()
   context.patients = get_patients()
   context.current_day = getdate(today()).strftime('%A')
   context.user = frappe.get_user().doc.full_name
   context.departments = get_department()
   context.deparment_endpoint = main_url
   context.search_url = search_url
   context.csrf_token = csrf_token
   return context