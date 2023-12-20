import frappe
from frappe import _
from frappe.utils import  getdate
from frappe.utils import add_days, add_months, cint, cstr, flt, formatdate, get_first_day, getdate
<<<<<<< HEAD

=======
from dynamic.future.financial_statements import validate_dates 
>>>>>>> b68437acb5951ab4f88a965e164979e776287914

import math
import re

def get_dates_labels(filters) :
   period_list = [] 
   start_date = filters.get("from_date") 
   start_date = f"{start_date[0:7]}-01"
   months_to_add = 1 
   months =  get_months(getdate(filters.get("from_date") ), getdate(filters.get("to_date")) )
   for i in range(cint(math.ceil(months / months_to_add))):
         period = frappe._dict({"from_date": getdate(start_date)})
         to_date = add_months(start_date, months_to_add)

         period.to_date  = getdate(add_days(to_date, -1))
         period_list.append(period)
         start_date = add_months(start_date , 1)
   for opts in period_list:
         key = opts["to_date"].strftime("%b_%Y").lower()
         label = formatdate(opts["to_date"], "MMM YYYY")
         opts.update(
			{
				"key": key.replace(" ", "_").replace("-", "_"),
				"label": label, 
            
         })
   return period_list
def execute(filters=None):
     columns, data = get_columns(filters), get_data(filters)
     return columns, data
def get_months(start_date, end_date):
	diff = (12 * end_date.year + end_date.month) - (12 * start_date.year + start_date.month)
	return diff + 1

def get_data(filters =None):
   data = []
   cost_centers = frappe.db.sql(""" 
   SELECT  a.cost_center  as cost_center  
   FROM `tabSales Invoice Item` a 
   INNER JOIN `tabSales Invoice` b 
   ON a.parent = b.name 
   WHERE b.docstatus = 1 
   GROUP BY cost_center
   """,as_dict=1)

   condetions = ""
   if filters.get("item") :
        condetions = condetions + f""" a.item_code  = '{filters.get("item")}' AND"""
   if filters.get("customer") :
        condetions = condetions + f""" b.customer = '{filters.get("customer")}' AND"""
   if filters.get("cost_center") :
        cost_centers = [{"cost_center" : filters.get("cost_center")}]
       
   if filters.get("warehouse") :
        condetions = condetions + f""" a.warehouse = '{filters.get("warehouse")}' AND"""  
   period_list = get_period_list(filters=filters)
   for cost in cost_centers :
      center ={"cost_center" : cost.get('cost_center')}
      for month in period_list :
         fil = frappe.db.sql(f""" SELECT  SUM(amount) as {month.get('key')} FROM 
             `tabSales Invoice Item`  a 
              INNER JOIN `tabSales Invoice` b 
              ON a.parent = b.name 
              WHERE 
              b.docstatus = 1 and
              a.cost_center = '{cost.get('cost_center')}' AND {condetions}
              b.posting_date > date('{month.get('from_date')}') AND b.posting_date < date('{month.get('to_date')}')
              """ ,as_dict=1)
         center[month.get('key')] = float (fil[0].get(month.get('key'))  or 0 )
      data.append(center)  
   return data
def get_columns(filters):
    period_list = get_period_list(filters=filters)
    columns =[
         { 
            "label": _("Cost Center"), 
            "fieldname": "cost_center", 
            "fieldtype": "Link", 
            "options": "Cost Center", 
            "width": 300, 
        }, 
         
    ]
    for period in period_list:
         columns.append(
			{
				"fieldname": period.key,
				"label": period.label,
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			}
		)
    return columns

def get_period_list(filters):
     period_start_date =filters.get("period_start_date")
     period_end_date =  filters.get("period_end_date")
     
     validate_dates(period_start_date, period_end_date)
     year_start_date = getdate(period_start_date)
     year_end_date = getdate(period_end_date)
     
     months_to_add = 1
     start_date = year_start_date
     months = get_months(year_start_date, year_end_date)
     period_list = []
     for i in range(cint(math.ceil(months / months_to_add))):
          period = frappe._dict({"from_date": start_date})
          
          if i == 0 :
               to_date = add_months(get_first_day(start_date), months_to_add)
          else:
               to_date = add_months(start_date, months_to_add)
          
          start_date = to_date

		# Subtract one day from to_date, as it may be first day in next fiscal year or month
          to_date = add_days(to_date, -1)
          
          if to_date <= year_end_date:
			# the normal case
               period.to_date = to_date
          else:
			# if a fiscal year ends before a 12 month period
               period.to_date = year_end_date
          
          period_list.append(period)
          
          if period.to_date == year_end_date:
               break
     for opts in period_list:
          key = opts["to_date"].strftime("%b_%Y").lower()
          label = opts["to_date"].strftime("%b %Y")
          opts.update(
			{
				"key": key.replace(" ", "_").replace("-", "_"),
				"label": label,
				"year_start_date": year_start_date,
				"year_end_date": year_end_date,
			}
		)
     return period_list
