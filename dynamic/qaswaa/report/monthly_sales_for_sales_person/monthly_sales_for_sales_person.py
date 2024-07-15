# Copyright (c) 2024, Dynamic and contributors
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
	conditions = ""
	if filters.get("cost_center") :
		conditions += f""" and si.cost_center = '{filters.get('cost_center')}' """
	if filters.get("warehouse"):
		conditions += f" and si.set_warehouse = '{filters.get('warehouse')}' "
	if filters.get("customer") :
		conditions += f""" and si.customer = "{filters.get('customer')}" """
	if filters.get("item_group") :
		conditions += f""" and sii.item_group = "{filters.get('item_group')}" """
	if filters.get("sales_person") :
		conditions += f""" and st.sales_person = "{filters.get('sales_person')}" """	

	period_list = get_period_list(filters)
	print(conditions)

	sql =  f'''
		SELECT 
			st.sales_person
		FROM 
			`tabSales Invoice Item` sii
		INNER JOIN 
			`tabSales Invoice` si
		ON 
			si.name = sii.parent
		INNER JOIN
			`tabSales Team` st
		ON
			si.name = st.parent
		WHERE 
			si.docstatus = 1
			AND 
			st.sales_person IS NOT NULL 
		GROUP BY 
			st.sales_person  ;
		'''
	results = []
	sales_persones = frappe.db.sql(sql , as_dict= 1)
	for sales_person in sales_persones :
		if filters.get("sales_person") and filters.get("sales_person") != sales_person.sales_person:
			continue
		dict ={"sales_person" : sales_person.sales_person}
		for period in period_list :

			ss = f"""
				SELECT 
					distinct si.name as name
				FROM 
					`tabSales Invoice Item` as sii
				INNER JOIN 
					`tabSales Invoice` as si
				ON 
					si.name = sii.parent
				LEFT JOIN
					`tabSales Team` as st
				ON
					si.name = st.parent
				WHERE
					si.docstatus = 1 
					and st.sales_person = '{sales_person.sales_person}' 
					and	si.posting_date >= '{period.from_date}' 
					and si.posting_date <= '{period.to_date}' 
					{conditions}  """
			data = frappe.db.sql(ss , as_list = 1)
			total = 0
			for r in data:
				invoice_doc = frappe.get_doc("Sales Invoice", r[0])
				total += invoice_doc.net_total or 0
			dict[period.key] = total

		results.append(dict)
	for record in results:
		total_sales = sum(value for value in record.values() if isinstance(value, (int, float)))
		record['total'] = total_sales
	return results

def get_columns(filters):
	period_list = get_period_list(filters)
	columns = [
		{
			"fieldname": "sales_person",
			"label": _("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person",
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
	columns.append(
			{
				"fieldname": "total",
				"label": "Total",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 100,
			}
	)

	return columns

