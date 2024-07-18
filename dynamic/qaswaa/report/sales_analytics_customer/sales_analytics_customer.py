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
    results = []
    customers = frappe.db.sql(sql , as_dict= 1)
    conditions = " 1=1"
    if filters.get("cost_center") :
        conditions += f" and SI.cost_center = '{filters.get('cost_center')}'"
    if filters.get("warehouse") :
        conditions += f" and SI.set_warehouse = '{filters.get('warehouse')}'"
    if filters.get("customer") :
        customers = [{"customer" : filters.get("customer")}]
        conditions += f" and SI.customer = '{filters.get('customer')}'"
    if filters.get("item_group") :
        conditions += f" and SII.item_group = '{filters.get('item_group')}'"
    if filters.get("item_code") :
        conditions += f" and SII.item_code = '{filters.get('item_code')}'"
    if filters.get("sales_person") :
        conditions += f" and ST.sales_person = '{filters.get('sales_person')}' "

    period_list = get_period_list(filters)
    for customer in customers :
        customer = customer["customer"]
        dict ={"customer" : customer}
        # conditions += f" and SII.cost_center = '{center}'"
        for period in period_list :

            ss = f'''
                SELECT 
                    DISTINCT SI.name as name
                FROM 
                    `tabSales Invoice` SI 
                INNER JOIN 
                    `tabSales Invoice Item` SII
                ON 
                    SI.name = SII.parent
                INNER JOIN
                    `tabSales Team` ST
                ON
                    SI.name = ST.parent
                WHERE
                    {conditions} and
                    SI.docstatus = 1 and
                    SI.customer = '{customer}' and 
                    SI.posting_date >= '{period.from_date}' 
                    and SI.posting_date <= '{period.to_date}'
                '''
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
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
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