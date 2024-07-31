import frappe
from frappe import _
from frappe.utils import  getdate
from frappe.utils import add_days, add_months, cint, cstr, flt, formatdate, get_first_day, getdate
from dynamic.future.financial_statements import validate_dates 
from frappe.utils import flt

import math
import re

def execute(filters=None):
     columns, data = get_columns(filters), get_data(filters)
     return columns, data


def get_months(start_date, end_date):
     diff = (12 * end_date.year + end_date.month) - (12 * start_date.year + start_date.month)
     return diff + 1
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
def get_data(filters=None):
    conditions = ""
    
    # Initialize filter for project if provided
    project_filter = ""
    if filters and 'project' in filters and filters['project']:
        project_filter = f"AND a.project = '{filters['project']}'"

    data = []
    
    # Fetching distinct projects and their associated customers
    projects_query = f"""
        SELECT a.project, a.customer
        FROM `tabSales Order` a
        WHERE a.docstatus != 2 
        AND a.project != ""
        {project_filter}
        GROUP BY a.project
    """
    
    projects = frappe.db.sql(projects_query, as_dict=1)

    # Get the list of periods to analyze
    period_list = get_period_list(filters=filters)
    
    for project in projects:
        project_name = project.get('project')
        customer = project.get('customer')
        
        # Initialize monthly totals dictionary
        monthly_totals = {month.get('key'): 0 for month in period_list} 

        for month in period_list:
            from_date = month.get('from_date')
            to_date = month.get('to_date')
            period_key = month.get('key')

            result = frappe.db.sql(f"""
                SELECT
                    SUM(a.advance_amount) AS total_advance_amount
                FROM `tabSales Invoice Advance` a
                INNER JOIN `tabSales Order` b ON a.parent = b.name
                WHERE
                    b.docstatus != 2
                    AND b.project = '{project_name}'
                    AND b.transaction_date >= DATE('{from_date}')
                    AND b.transaction_date <= DATE('{to_date}')
                    {conditions}
            """, as_dict=1)

            # Safeguard against None values
            total_advance_amount = result[0].get('total_advance_amount', 0) if result else 0
            
            # Update the monthly totals
            monthly_totals[period_key] = total_advance_amount
        
        # Fetch the item codes from the Sales Order Item child table
        item_codes_query = f"""
            SELECT DISTINCT b.item_code
            FROM `tabSales Order Item` b
            INNER JOIN `tabSales Order` a ON a.name = b.parent
            WHERE a.project = '{project_name}'
        """
        
        item_codes = frappe.db.sql(item_codes_query, as_dict=1)
        item_codes_list = [item.get('item_code') for item in item_codes]
        
        # Calculate the total sum of all monthly totals
        total_sum = sum(value for value in monthly_totals.values() if isinstance(value, (int, float)))

        # Append the data for the current project
        data.append({
            'customer': customer,
            'project': project_name,
            'item_codes': ', '.join(item_codes_list),  # Add item codes to data
            **monthly_totals,
            'total': total_sum  # Add total sum to data
        })
    
    return data




def get_columns(filters):
    period_list = get_period_list(filters=filters)
    columns = [
        {
            "label": _("Project"),
            "fieldname": "project",
            "fieldtype": "Link",
            "options": "Project",
            "width": 200,
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200,
        },
        {
            "label": _("Units"),
            "fieldname": "item_codes",
            "fieldtype": "Data",
            "width": 200,
        },
    ]
    
    for period in period_list:
        columns.append(
            {
                "fieldname": period.key,
                "label": period.label,
                "fieldtype": "Currency",
                "options": "party_account_currency",
                "width": 150,
            }
        )

    # Add total column
    columns.append(
        {
            "fieldname": "total",
            "label": _("Total"),
            "fieldtype": "Currency",
            "options": "party_account_currency",
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