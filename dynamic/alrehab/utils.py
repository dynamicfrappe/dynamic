import frappe 
from frappe.utils import today
from datetime import date
from frappe.utils import (
	cint,
	cstr,
	flt,
	fmt_money,
	format_datetime,
	format_duration,
	format_time,
	format_timedelta,
	formatdate,
	getdate,
)

@frappe.whitelist()
def caculate_installment_value(entry):
   eq_string= ""
   doc = frappe.get_doc("installment Entry" , entry)
   # print(f'\n\n\n entry.name==>{entry.name}')
   if not doc.ignore_delay_penalty:
      area_c = frappe.db.get_value('Customer', doc.customer , 'unit_area')
      pay_template = frappe.get_doc("installment Entry Type" , doc.type)
      penality_template = False
      if pay_template.financial_penalty_template  and pay_template.delay_penalty:
         penality_template  = frappe.get_doc("Financial penalty template" , pay_template.financial_penalty_template)
      if penality_template :
         if penality_template.auto_create:
            equation_value = flt(penality_template.creation_frequency) * flt(penality_template.monthly)
         if penality_template.equation :
            variables = [i for i in penality_template.variables]
            # change string values with current value 
            for a in penality_template.equation :
               if a.isalnum() :
               #caculate a 
                  for  i in variables :
                     if i.variable == a :
                        if i.filed == "Static Value":
                           eq_string = eq_string +  i.value
                           # print(f'\n\n\n eq_string++==>{eq_string}')
                        if i.filed=="Item Unit Value" :
                           eq_string = eq_string + f"{area_c}"
                        if i.filed=="Days" :
                           #caculate days 
                           c_days= 1 
                           date_diff = date.today() - doc.due_date 
                           eq_string = eq_string + f"{date_diff.days}" 	
               else :
                  eq_string = eq_string +  a
            equation_value = eval(eq_string) or 0
         out_stand = 0
         if equation_value:
            entry.db_set('delay_penalty',equation_value)
            if not entry.outstanding_value:
               out_stand = (float(entry.total_value or 0) + float(equation_value)) - float(entry.total_payed or 0)
            if float(entry.outstanding_value or 0):
               out_stand = float(entry.outstanding_value or 0) + float(equation_value)
            entry.db_set('outstanding_value',out_stand)