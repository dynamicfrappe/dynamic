import frappe
from frappe import _
from frappe.utils import  getdate
from frappe.utils import add_days, add_months, cint, cstr, flt, formatdate, get_first_day, getdate


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
   GROUP BY cost_center
   """,as_dict=1)
   mais_sql = ""
   monthes = get_dates_labels(filters)
   for cost in cost_centers :
      center ={"cost_center" : cost.get('cost_center')}
      for month in monthes :
         fil = frappe.db.sql(f""" SELECT  SUM(a.base_amount) as {month.get("key")} FROM 
             `tabSales Invoice Item`  a 
              INNER JOIN `tabSales Invoice` b 
              ON a.parent = b.name 
              WHERE a.cost_center = '{cost.get('cost_center')}' AND 
              b.posting_date > date('{month.get("from_date")}') AND b.posting_date < date('{month.get("to_date")}')
              """ ,as_dict=1)
         center[month.get("key")] = float (fil[0].get(month.get("key"))  or 0 )
      data.append(center)  
   print("data", data )
   # data = cost_centers
   return data
def get_columns(filters):
    ex_col = get_dates_labels(filters=filters)
    columns =[
         { 
            "label": _("Cost Center"), 
            "fieldname": "cost_center", 
            "fieldtype": "Link", 
            "options": "Cost Center", 
            "width": 100, 
        }, 
         
    ]
    for col in ex_col :
         columns.append({
              "label":_(col.get("label")) ,
              "fieldname" : f"""{col.get("key")}""" ,
              "fieldtype" :"Data"
         })
    return columns