# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils import flt
import collections, functools, operator
#dynamic.dynamic.report.p_and_l_cost_center.utils
from dynamic.dynamic.report.p_and_l_cost_center.utils import (
	get_columns,
	get_data,
	get_filtered_list_for_consolidated_report,
	get_period_list,
	get_cost_of_good_sold_data
)
# from dynamic.future.financial_statements import (
# 	get_columns,
# 	get_data,
# 	get_filtered_list_for_consolidated_report,
# 	get_period_list,
# 	get_cost_of_good_sold_data
# )

all_incom_list = []
all_expense_list = []

def execute(filters=None):
	data = []
	
	period_list = get_period_list(
			filters.from_fiscal_year,
			filters.to_fiscal_year,
			filters.period_start_date,
			filters.period_end_date,
			filters.filter_based_on,
			filters.periodicity,
			company=filters.company,
		)
	total_income = total_expense=0
	for cost_center in filters.get("cost_center") : 
		data.extend( [
	# 		{
    #     "account":  f"___________" ,
    #     "parent_account":   "",
    #     "indent": "" ,
        
    #   } ,
			
			{
        "account":  f"{cost_center}" ,
        "parent_account":   "",
        "indent": "" ,
        
      } ,{ 
        "account":  f"___________" ,
        "parent_account":   "",
        "indent": "" ,
        
      } ,
		
		
		
		
		])
		period_list = get_period_list(
			filters.from_fiscal_year,
			filters.to_fiscal_year,
			filters.period_start_date,
			filters.period_end_date,
			filters.filter_based_on,
			filters.periodicity,
			company=filters.company,
		)

		income = get_data(
			filters.company,
			"Income",
			"Credit",
			period_list,
			cost_center,
			filters=filters,
			accumulated_values=filters.accumulated_values,
			ignore_closing_entries=True,
			ignore_accumulated_values_for_fy=True,
		)
		cost_of_good_sold = get_cost_of_good_sold_data(
			filters.company,
			filters.get("account"),
			"Debit",
			period_list,
			cost_center, 
			filters=filters,
			accumulated_values=filters.accumulated_values,
			ignore_closing_entries=True,
			ignore_accumulated_values_for_fy=True,
		)
		# print("cost_of_good_sold ------------------------> ",cost_of_good_sold)

		expense = get_data(
			filters.company,
			"Expense",
			"Debit",
			period_list,
			cost_center,
			filters=filters,
			accumulated_values=filters.accumulated_values,
			ignore_closing_entries=True,
			ignore_accumulated_values_for_fy=True,
			
		)
		new_expense = []
		for i in expense :
			if i not in  cost_of_good_sold and i.get("account") != filters.get("account"):
				# expense.remove(i)
				new_expense.append(i)
			
				
		#fileter expense
		# print("Expence" , expense )

		net_profit_loss = get_net_profit_loss(
			income, new_expense , period_list, filters.company, filters.presentation_currency
		)
		# print("income",income)
		# print("cost_of_good_sold",cost_of_good_sold)
		if len(cost_of_good_sold) > 0:
			total_income_againest_cost_of_good_sold = {
				'account_name': 'Gross Profit',
				'account': 'Gross Profit', 
				'currency': 'EGP',
				'opening_balance': 0.0,
				'dec_2023': income[len(income)-2].get("total") - cost_of_good_sold[len(cost_of_good_sold)-2].get("total"),
				'total': income[len(income)-2].get("total") - cost_of_good_sold[len(cost_of_good_sold)-2].get("total")
			}
			cost_of_good_sold.append(total_income_againest_cost_of_good_sold)
		

		# cost_centers = filters.get("cost_center")
		# frappe.errprint(f'incom:{income}')
		# frappe.errprint(f'expense:{expense}')
		data.extend(income or [])
		data.extend(cost_of_good_sold or [])
		data.extend(new_expense or [])

		# for row in 
		if net_profit_loss:
			data.append(net_profit_loss)
		
		#?add new row
	net_income_loss,net_expense_loss, submition = add_total_colms(all_incom_list, all_expense_list , period_list, filters.company, filters.presentation_currency)
	data.append(net_income_loss)
	data.append(net_expense_loss)
	data.append(submition)
	# frappe.errprint(f'all_incom_list=======:{all_incom_list}')
	columns = get_columns(
		filters.periodicity, period_list, filters.accumulated_values, filters.company
	)

	chart =[] 
	# if filters.get("chart") :
	# 	chart = get_chart_data(filters, columns, income, expense, net_profit_loss)

	currency = filters.presentation_currency or frappe.get_cached_value(
		"Company", filters.company, "default_currency"
	)
	report_summary = [] # 
	"""get_report_summary(
		period_list, filters.periodicity, income, expense, net_profit_loss, currency, filters
	) """

	return columns, data, None, chart, report_summary


def get_report_summary(
	period_list, periodicity, income, expense, net_profit_loss, currency, filters, consolidated=False
):
	
	return [

	]
	net_income, net_expense, net_profit = 0.0, 0.0, 0.0

	# from consolidated financial statement
	if filters.get("accumulated_in_group_company"):
		period_list = get_filtered_list_for_consolidated_report(filters, period_list)

	for period in period_list:
		key = period if consolidated else period.key
		if income:
			net_income += income[-2].get(key)
		if expense:
			net_expense += expense[-2].get(key)
		if net_profit_loss:
			net_profit += net_profit_loss.get(key)

	if len(period_list) == 1 and periodicity == "Yearly":
		profit_label = _("Profit This Year ")
		income_label = _("Total Income This Year")
		expense_label = _("Total Expense This Year")
	else:
		profit_label = _("Net Profit")
		income_label = _("Total Income")
		expense_label = _("Total Expense")

	return [
		{"value": net_income, "label": income_label, "datatype": "Currency", "currency": currency},
		{"type": "separator", "value": "-"},
		{"value": net_expense, "label": expense_label, "datatype": "Currency", "currency": currency},
		{"type": "separator", "value": "=", "color": "blue"},
		{
			"value": net_profit,
			"indicator": "Green" if net_profit > 0 else "Red",
			"label": profit_label,
			"datatype": "Currency",
			"currency": currency,
		},
	]


def get_net_profit_loss(income, expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
		"account_name": "'" + _("Profit for the year") + "'",
		"account": "'" + _("Profit for the year") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
	}
	row_incom = {}
	row_expense = {}

	has_value = False
	# print(f"all Expencies ==========   {expense}")
	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2][key], 3) if income else 0
		total_expense = flt(expense[-1][key], 3) if expense else 0
		# print(f"Exception ------- {flt(expense[-1][key], 3) }")
		net_profit_loss[key] = total_income - total_expense

		row_incom[key] = total_income 
		row_expense[key] =  total_expense

		if net_profit_loss[key]:
			has_value = True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total
	
	all_incom_list.append(row_incom)
	all_expense_list.append(row_expense)
	# frappe.errprint(f'get_net_profit_loss==>{net_profit_loss}')
	if has_value:
		return net_profit_loss

def add_total_colms(all_incom, all_expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_income_loss = {
		"account_name": "'" + _("All Income") + "'",
		"account": "'" + _("All Income") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
	}

	net_expense_loss = {
		"account_name": "'" + _("All Expense") + "'",
		"account": "'" + _("All Expense") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
	}

	submition = {
		"account_name": "'" + _("Total Profit Or Loss") + "'",
		"account": "'" + _("Total Profit Or Loss") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
	}

	has_value = False
	result_income = {}
	result_income_row = {}
	result_expense_row = {}
	diff_dict = {}
	#** all_income
	if all_incom:
		result_income = dict(functools.reduce(operator.add,map(collections.Counter, all_incom)))
		result_income_row = {**net_income_loss, **result_income}
	#** all_expense
	if all_expense:
		result_expense = dict(functools.reduce(operator.add,map(collections.Counter, all_expense)))
		result_expense_row = {**net_expense_loss, **result_expense}
	#** subtract
	if result_income:
		for key in result_income.keys():
			diff_dict[key] = result_income.get(key, 0) - result_expense.get(key, 0)
	submition = {**submition, **diff_dict}
	# frappe.errprint(f'result==>{result}')
	return result_income_row or [], result_expense_row or [], submition or []



def get_chart_data(filters, columns, income, expense, net_profit_loss):
	labels = [d.get("label") for d in columns[2:]]

	income_data, expense_data, net_profit = [], [], []

	for p in columns[2:]:
		if income:
			income_data.append(income[-2].get(p.get("fieldname")))
		if expense:
			expense_data.append(expense[-2].get(p.get("fieldname")))
		if net_profit_loss:
			net_profit.append(net_profit_loss.get(p.get("fieldname")))

	datasets = []
	if income_data:
		datasets.append({"name": _("Income"), "values": income_data})
	if expense_data:
		datasets.append({"name": _("Expense"), "values": expense_data})
	if net_profit:
		datasets.append({"name": _("Net Profit/Loss"), "values": net_profit})

	chart = {"data": {"labels": labels, "datasets": datasets}}

	if not filters.accumulated_values:
		chart["type"] = "bar"
	else:
		chart["type"] = "line"

	chart["fieldtype"] = "Currency"

	return chart
