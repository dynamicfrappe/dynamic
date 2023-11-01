import frappe 
from frappe.utils import today
#dynamic.alrehab.utils
#/home/beshoy/Dynamic-13/tera/frappe-tera/apps/dynamic/dynamic/alrehab/utils.py
#from dynamic.alrehab.utils import caculate_installment_value
#caculate_installment_value('f8ba170d05')




@frappe.whitelist()
def caculate_installment_value(entry):
   #get entry 
   # get penality template from type 
   eq_string= ""
   doc = frappe.get_doc("installment Entry" , entry)
   area_c = frappe.db.get_value('Customer', doc.customer , 'unit_area')
   pay_template = frappe.get_doc("installment Entry Type" , doc.type)
   penality_template = False
   if pay_template.financial_penalty_template :
      penality_template  = frappe.get_doc("Financial penalty template" , pay_template.financial_penalty_template)
   if penality_template :
      if penality_template.equation :
         variables = [i for i in penality_template.variables]
         #caculate equation variables 
         # change string values with current value 
         for a in penality_template.equation :
            if a.isalnum() :
               #caculate a 
               for  i in variables :
                  print(i)
                  if i.variable == a :
                    if i.filed == "Static Value":
                       eq_string = eq_string +  i.value
                    if i.filed=="Item Unit Value" :
                       eq_string = eq_string + f"{area_c}"
                    if i.filed=="Days" :
                       #caculate days 
                       c_days= 1 
                       eq_string = eq_string + f"{c_days}" 
                     
               pass
            else :
              eq_string = eq_string +  a
         pass
      print(eq_string)
      # df = 0
      df = exec("df =(10/12) *( 1*150)")
      print(f" value , {df} ")
   #caculate equation 
