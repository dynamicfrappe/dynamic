# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import math
from dynamic.future.financial_statements import (
	get_period_list,
	validate_dates , 
	get_months,
	get_label
)
from frappe.utils import getdate , cint , add_months, get_first_day , add_days , formatdate

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

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


def get_data(filters):
	conditions = " 1=1"
	if filters.get("cost_center") :
		conditions += f" and SII.cost_center = '{filters.get('cost_center')}'"
	if filters.get("warehouse") :
		conditions += f" and SII.warehouse = '{filters.get('warehouse')}'"
	if filters.get("customer") :
		conditions += f" and SI.customer = '{filters.get('customer')}'"
	if filters.get("item_group") :
		conditions += f" and SII.item_group = '{filters.get('item_group')}'"
	if filters.get("item_code") :
		conditions += f" and SII.item_code = '{filters.get('item_code')}'"

	period_list = get_period_list(filters)

	# if filters.get("cost_center") :
	sql =  f'''
		SELECT 
			SI.sales_partner 
		FROM 
			`tabSales Invoice` SI 
		INNER JOIN 
			`tabSales Invoice Item` SII
		ON 
			SI.name = SII.parent
		WHERE 
			SI.docstatus = 1
			AND 
			SI.sales_partner IS NOT NULL
		GROUP BY 
			SI.sales_partner  
		'''
	results = []
	parteners = frappe.db.sql(sql , as_dict= 1)
	for partener in parteners :
		partener = partener.sales_partner
		dict ={"sales_partner" : partener}
		# conditions += f" and SII.cost_center = '{center}'"
		for period in period_list :

			ss = f'''
				SELECT 
					SUM(SII.amount) as {period.key}
				FROM 
					`tabSales Invoice` SI 
				INNER JOIN 
					`tabSales Invoice Item` SII
				ON 
					SI.name = SII.parent
				WHERE
				    {conditions} and
					SI.docstatus = 1 and
					SI.sales_partner = '{partener}' and 
					SI.posting_date >= '{period.from_date}' 
					and SI.posting_date <= '{period.to_date}'
				'''
								# , ST.sales_person
				# 			LEFT JOIN 
				# 	`tabSales Team` ST
				# ON
				# 	ST.parent = SI.name
			data = frappe.db.sql(ss , as_dict = 1)
			dict[period.key] = data[0][period.key]

		results.append(dict)
	return results

def get_columns(filters):
	period_list = get_period_list(filters)
	columns = [
		{
			"fieldname": "sales_partner",
			"label": _("Sales Partner"),
			"fieldtype": "Link",
			"options": "Sales Partner",
			"width": 300,
		},
		# {
		# 	"fieldname": "sales_person",
		# 	"label": _("Sales Person"),
		# 	"fieldtype": "Link",
		# 	"options": "Sales Person",
		# 	"width": 300,
		# },
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
