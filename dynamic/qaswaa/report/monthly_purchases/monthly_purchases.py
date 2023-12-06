# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import math
from dynamic.future.financial_statements import (
	get_columns,
	get_data,
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
	periodicity = filters.get("periodicity")

	validate_dates(period_start_date, period_end_date)
	year_start_date = getdate(period_start_date)
	year_end_date = getdate(period_end_date)

	months_to_add = {"Yearly": 12, "Half-Yearly": 6, "Quarterly": 3, "Monthly": 1}[periodicity]

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
	# frappe.throw(str(period_list))
	for opts in period_list:
		key = opts["to_date"].strftime("%b_%Y").lower()
		if periodicity == "Monthly":
			label = formatdate(opts["to_date"], "MMM YYYY")
		else:
			label = get_label(periodicity, opts["from_date"], opts["to_date"])

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

	period_list = get_period_list(filters)

	# if filters.get("cost_center") :
	sql =  f'''
		SELECT 
			PII.cost_center 
		FROM 
			`tabPurchase Invoice` PI 
		INNER JOIN 
			`tabPurchase Invoice Item` PII
		ON 
			PI.name = PII.parent
		WHERE 
			PI.docstatus = 1
		GROUP BY 
			PII.cost_center
		'''
	results = []
	cost_center = frappe.db.sql(sql , as_dict= 1)
	for center in cost_center :
		center = center.cost_center
		dict ={"cost_center" : center}
		conditions += f" and PII.cost_center = '{center}'"
		for period in period_list :
			conditions += f" and PI.posting_date >= '{period.from_date}' and PI.posting_date <= '{period.to_date}'"
			ss = f'''
				SELECT 
					SUM(PII.amount) as {period.key}
				FROM 
					`tabPurchase Invoice` PI 
				INNER JOIN 
					`tabPurchase Invoice Item` PII
				ON 
					PI.name = PII.parent
				WHERE
					{conditions}
				'''
			data = frappe.db.sql(ss , as_dict = 1)
			dict[period.key] = data[0][period.key]

		results.append(dict)
	return results

def get_columns( filters):
	periodicity = filters.get("periodicity")
	period_list = get_period_list(filters)
	columns = [
		{
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 300,
		}
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
	if periodicity != "Yearly":
			columns.append(
				{"fieldname": "total", "label": _("Total"), "fieldtype": "Currency", "width": 150}
			)
	return columns
