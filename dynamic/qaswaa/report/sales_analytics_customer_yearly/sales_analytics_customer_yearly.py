# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import math
from dynamic.future.financial_statements import (
	get_period_list,
	validate_dates , 
	get_months,
)
from frappe.utils import getdate , cint , add_months, get_first_day , add_days 

def execute(filters=None):

	
	columns, data = get_columns(filters), []
	return columns, data

def get_months_in_year_range(start_year, end_year):
		if start_year > end_year:
			raise ValueError("Start year must be less than or equal to end year")

		# Define a static list of month names with labels, values, and year
		months_in_range = []
		for year in range(start_year, end_year + 1):
			for month in range(1, 13):
				month_info = {
					"label": _("{0} {1}").format(_("Month"), month),
					"value": month,
					"year": year,
				}
				months_in_range.append(month_info)
		# frappe.throw(str(months_in_range))
		return months_in_range

# def get_static_months():
#     # Define a static list of month names
# 	months = [{"label" : "January" , "value" : 1},
# 		     {"label" : "February" , "value" : 2},
# 			 {"label" : "March" , "value" : 3},
# 			 {"label" : "April" , "value" : 4},
# 			 {"label" : "May" , "value" : 5},
# 			 {"label" : "June" , "value" : 6},
# 			 {"label" : "July" , "value" : 7},
# 			 {"label" : "August" , "value" : 8},
# 			 ]
#     months = [
#         _("January"),
#         _("February"),
#         _("March"),
#         _("April"),
#         _("May"),
#         _("June"),
#         _("July"),
#         _("August"),
#         _("September"),
#         _("October"),
#         _("November"),
#         _("December"),
#     ]

#     return months














# def get_period_list(filters):
# 	period_start_date =filters.get("period_start_date")
# 	period_end_date =  filters.get("period_end_date")

# 	validate_dates(period_start_date, period_end_date)
# 	year_start_date = getdate(period_start_date)
# 	year_end_date = getdate(period_end_date)

# 	months_to_add = 1

# 	start_date = year_start_date
# 	months = get_months(year_start_date, year_end_date)
# 	period_list = []

# 	for i in range(cint(math.ceil(months / months_to_add))):
# 		period = frappe._dict({"from_date": start_date})

# 		if i == 0 :
# 			to_date = add_months(get_first_day(start_date), months_to_add)
# 		else:
# 			to_date = add_months(start_date, months_to_add)

# 		start_date = to_date

# 		# Subtract one day from to_date, as it may be first day in next fiscal year or month
# 		to_date = add_days(to_date, -1)

# 		if to_date <= year_end_date:
# 			# the normal case
# 			period.to_date = to_date
# 		else:
# 			# if a fiscal year ends before a 12 month period
# 			period.to_date = year_end_date

# 		period_list.append(period)

# 		if period.to_date == year_end_date:
# 			break
# 	for opts in period_list:
# 		key = opts["to_date"].strftime("%b_%Y").lower()
# 		label = opts["to_date"].strftime("%b %Y")
# 		opts.update(
# 			{
# 				"key": key.replace(" ", "_").replace("-", "_"),
# 				"label": label,
# 				"year_start_date": year_start_date,
# 				"year_end_date": year_end_date,
# 			}
# 		)
# 	return period_list


# def get_data(filters):
# 	sql =  f'''
# 		SELECT 
# 			SI.customer 
# 		FROM 
# 			`tabSales Invoice` SI 
# 		INNER JOIN 
# 			`tabSales Invoice Item` SII
# 		ON 
# 			SI.name = SII.parent
# 		WHERE 
# 			SI.docstatus = 1
# 		GROUP BY 
# 			SI.customer  
# 		'''
# 	results = []
# 	customers = frappe.db.sql(sql , as_dict= 1)
# 	conditions = " 1=1"
# 	if filters.get("cost_center") :
# 		conditions += f" and SII.cost_center = '{filters.get('cost_center')}'"
# 	if filters.get("warehouse") :
# 		conditions += f" and SII.warehouse = '{filters.get('warehouse')}'"
# 	if filters.get("customer") :
# 		customers = [{"customer" : filters.get("customer")}]
# 	if filters.get("item_group") :
# 		conditions += f" and SII.item_group = '{filters.get('item_group')}'"
# 	if filters.get("item_code") :
# 		conditions += f" and SII.item_code = '{filters.get('item_code')}'"

# 	period_list = get_period_list(filters)
# 	for customer in customers :
# 		customer = customer["customer"]
# 		dict ={"customer" : customer}
# 		# conditions += f" and SII.cost_center = '{center}'"
# 		for period in period_list :

# 			ss = f'''
# 				SELECT 
# 					SUM(SII.amount) as {period.key}
# 				FROM 
# 					`tabSales Invoice` SI 
# 				INNER JOIN 
# 					`tabSales Invoice Item` SII
# 				ON 
# 					SI.name = SII.parent
# 				WHERE
# 				    {conditions} and
# 					SI.docstatus = 1 and
# 					SI.customer = '{customer}' and 
# 					SI.posting_date >= '{period.from_date}' 
# 					and SI.posting_date <= '{period.to_date}'
# 				'''
# 			data = frappe.db.sql(ss , as_dict = 1)
# 			dict[period.key] = data[0][period.key]

# 		results.append(dict)
# 	return results

def get_columns(filters):
	period_list = get_months_in_year_range( 2022,2023)
	columns = [
		# {
		# 	"fieldname": "customer",
		# 	"label": _("Customer"),
		# 	"fieldtype": "Link",
		# 	"options": "Customer",
		# 	"width": 300,
		# },
	]
	for period in period_list:
		# frappe.throw(str(period["label"]))
		columns.append(
			{
				"fieldname": period["label"],
				"label": period["label"],
				"fieldtype": "Currency",
				"options": "currency",
				"width": 150,
			}
		)
	# frappe.throw(str(columns))
	return columns