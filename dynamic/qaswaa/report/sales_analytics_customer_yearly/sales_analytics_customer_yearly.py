# Copyright (c) 2023, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import math

from datetime import datetime, timedelta


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_years_between(fiiters):
	start_year_str , end_year_str = validate_year(fiiters)
	start_year = int(start_year_str)
	end_year = int(end_year_str)
	years_list = [str(year) for year in range(start_year, end_year + 1)]
	return years_list

def validate_year(filters):
	if filters.get("fiscal_year_start") and filters.get("fiscal_year_end"):
		fiscal_year_start = filters.get("fiscal_year_start")
		fiscal_year_end = filters.get("fiscal_year_end")
		if fiscal_year_start > fiscal_year_end :
			frappe.throw("Fiscal Year Start must be before Fiscal Year End")
		return fiscal_year_start , fiscal_year_end
	
def get_all_months(year_str):
    year = int(year_str)
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    all_months = []
    current_month = start_date

    while current_month <= end_date:
        next_month = current_month.replace(day=1) + timedelta(days=32)  # Move to the first day of the next month
        next_month = next_month.replace(day=1) - timedelta(days=1)  # Move back one day to get the last day of the current month

        month_data = {
            f'month': current_month.strftime("%B"),
            'from_date': current_month.strftime("%Y-%m-%d"),
            'to_date': next_month.strftime("%Y-%m-%d"),
        }
        all_months.append(month_data)
        current_month = next_month + timedelta(days=1)  # Move to the next day to start the next month

    return all_months
    

def get_data(filters):
	result = []
	sql =  f'''
		SELECT 
			SI.customer 
		FROM 
			`tabSales Invoice` SI 
		INNER JOIN 
			`tabSales Invoice Item` SII
		ON 
			SI.name = SII.parent
		WHERE 
			SI.docstatus = 1
		GROUP BY 
			SI.customer  
		'''
	customers = frappe.db.sql(sql , as_dict= 1)
	conditions = " 1=1"
	if filters.get("cost_center") :
		conditions += f" and SII.cost_center = '{filters.get('cost_center')}'"
	if filters.get("customer") :
		customers = [{"customer" : filters.get("customer")}]
		# conditions += f" and SI.customer = '{filters.get('customer')}'"
	if filters.get("item_group") :
		conditions += f" and SII.item_group = '{filters.get('item_group')}'"
	if filters.get("item_code") :
		conditions += f" and SII.item_code = '{filters.get('item_code')}'"

	for customer in customers :
		customer = customer["customer"]
		years = get_years_between(filters)
		for year in years : 
			dict = {}
			dict["customer"] = customer			
			dict["year"] = f'{year}'

			period_list =get_all_months(year)
			for period in period_list:
				ss = f'''
					SELECT 
						SI.customer , 
						SUM(SII.amount) as {period["month"]}
					FROM 
						`tabSales Invoice` SI 
					INNER JOIN 
						`tabSales Invoice Item` SII
					ON 
						SI.name = SII.parent
					WHERE
						SI.docstatus = 1 and
						SI.customer = '{customer}' and 
						SI.posting_date >= '{period['from_date']}'
						and SI.posting_date <= '{period['to_date']}'
					'''
				data = frappe.db.sql(ss , as_dict = 1)
				dict[f'{period["month"]}']= data[0][f'{period["month"]}']
			result.append(dict)

	return result


def get_columns(filters):
	columns = []
	years = get_years_between(filters)
	for year in years :
		columns.append(
			{
				"fieldname": "year",
				"label": _("Year"),
				"fieldtype": "Data",
				"width": 300,
			},
		)
		columns.append(
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 300,
		},
	    )
		period_list =get_all_months(year)
		for period in period_list:
			columns.append(
				{
					"fieldname": period["month"],
					"label": period["month"],
					"fieldtype": "Currency",
					"options": "currency",
					"width": 150,
				}
			)
		return columns