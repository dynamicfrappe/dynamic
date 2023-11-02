import frappe 
from frappe.utils import today
from datetime import date
#dynamic.alrehab.utils
#/home/beshoy/Dynamic-13/tera/frappe-tera/apps/dynamic/dynamic/alrehab/utils.py
#from dynamic.alrehab.utils import caculate_installment_value
#caculate_installment_value('f8ba170d05')



@frappe.whitelist()
def caculate_installment_value(entry):
   # entry = frappe.get_doc('')
   #get entry 
   # get penality template from type 
   eq_string= ""
   doc = frappe.get_doc("installment Entry" , entry)
   if not doc.ignore_delay_penalty:
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
                     # print(f'\n\n\n\n==i==>{i} \n\n')
                     if i.variable == a :
                     if i.filed == "Static Value":
                        eq_string = eq_string +  i.value
                     if i.filed=="Item Unit Value" :
                        eq_string = eq_string + f"{area_c}"
                     if i.filed=="Days" :
                        #caculate days 
                        c_days= 1 
                        #diff days = now() - doc.due_date
                        date_diff = date.today() - doc.due_date 
                        eq_string = eq_string + f"{date_diff.days}" 
                        
                  pass
               else :
               eq_string = eq_string +  a
            pass
         equation_value = eval(eq_string) or 0
         if equation_value:
            doc.db_set('delay_penalty',equation_value)
            out_stand = (floar(doc.total_value or 0) + float(equation_value)) - float(doc.total_payed or 0)
            doc.db_set('outstanding_value',out_stand)
