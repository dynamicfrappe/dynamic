# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _
from frappe.utils import flt

from dynamic.future.financial_statements import (
	get_columns,
	get_data,
	get_filtered_list_for_consolidated_report,
	get_period_list,
	get_cost_of_good_sold_data
)

# total_income={}
# total_expense={}

def execute(filters=None):
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
		filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True,
		ignore_accumulated_values_for_fy=True,
	)
	# print(" \n\n cost_of_good_sold ------------------------> ",cost_of_good_sold ,'\n')

	#[{'account': '411 - تكلفة المبيعات - FW', 'parent_account': '', 'indent': 0.0, 'year_start_date': '2023-01-01', 'year_end_date': '2023-12-31', 'currency': 'EGP', 'include_in_gross': 0, 'account_type': 'Cost of Goods Sold', 'is_group': 0, 'opening_balance': 0.0, 'account_name': '411 - تكلفة المبيعات ', 'dec_2023': 8115322.58, 'has_value': True, 'total': 8115322.58}, {'account_name': 'Total 411 - تكلفة المبيعات - FW (Debit)', 'account': 'Total 411 - تكلفة المبيعات - FW (Debit)', 'currency': 'EGP', 'opening_balance': 0.0, 'dec_2023': 8115322.58, 'total': 8115322.58}, {}]

	expense = get_data(
		filters.company,
		"Expense",
		"Debit",
		period_list,
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

	# print("\n\n\nnew_expense ----/////--------------------> ",new_expense,'\n')
		
			

	# print("\n\n\n new_expense \n\n==>", new_expense )	
	gross_profit = get_total_profit_new(income, cost_of_good_sold , period_list, filters.company, filters.presentation_currency)

	net_profit_loss = get_net_profit_loss(
		income, new_expense , period_list, filters.company, filters.presentation_currency
	)
	
	data = []
	data.extend(income or [])
	data.extend(cost_of_good_sold or [])
	#** gross_profit
	data.append(gross_profit or [])
	data.extend(new_expense or [])
	
	if net_profit_loss:
		data.append(net_profit_loss)

	columns = get_columns(
		filters.periodicity, period_list, filters.accumulated_values, filters.company
	)

	# chart =[] 
	# if filters.get("chart") :
	# 	chart = get_chart_data(filters, columns, income, expense, net_profit_loss)

	currency = filters.presentation_currency or frappe.get_cached_value(
		"Company", filters.company, "default_currency"
	)
	# report_summary = get_report_summary(
	# 	period_list, filters.periodicity, income, expense, net_profit_loss, currency, filters
	# )

	return columns, data, None, None, None

def get_total_profit_new(income, expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
		"account_name": "'" + _("Gross Profit++--") + "'",
		"account": "'" + _("Gross Profit") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
	}
	row_incom = {}
	row_expense = {}
	total_income_increase = 0
	total_expense_increase = 0

	has_value = False
	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2][key], 3) if income else 0
		total_expense = flt(expense[-2][key], 3) if expense else 0
		# total_income_increase += flt(income[-2][key], 3) if income else 0
		# total_expense_increase +=  flt(expense[-2][key], 3) if expense else 0
		net_profit_loss[key] = total_income - total_expense


		if net_profit_loss[key]:
			has_value = True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total
	# frappe.errprint(f'total_income_increase==> {total_income_increase}')
	# frappe.errprint(f'total_expense_increase==> {total_expense_increase}')
	if has_value:
		return net_profit_loss

def get_report_summary(
	period_list, periodicity, income, expense, net_profit_loss, currency, filters, consolidated=False
):
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
		profit_label = _("Profit This Year")
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
	incom_total = 0
	exp_total = 0
	net_profit_loss = {
		"account_name": "'" + _("Profit for the year") + "'",
		"account": "'" + _("Profit for the year") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value("Company", company, "default_currency"),
	}
	has_value = False
	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2].get(key), 3) if income else 0
		# incom_total += flt(income[-2].get(key), 3) if income else 0
		total_expense = flt(expense[-2].get(key), 3) if expense else 0
		# exp_total += flt(expense[-1].get(key), 3) if expense else 0
		net_profit_loss[key] = total_income - total_expense

		if net_profit_loss[key]:
			has_value = True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total
	# frappe.errprint(f"all total ==========   {total}")
	# frappe.errprint(f" incom_total ==========   {incom_total}")
	# frappe.errprint(f" exp_total ==========   {exp_total}")
	

	if has_value:
		return net_profit_loss

