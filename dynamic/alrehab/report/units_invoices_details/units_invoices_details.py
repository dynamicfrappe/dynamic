# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, date_diff, flt
from datetime import datetime, date
from frappe.utils import getdate

def execute(filters=None):
	columns, data = [], []
	
	# columns = [
	# 	{"label": _("Unit"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
	# 	{"label": _("Area"), "fieldname": "unit_area", "fieldtype": "Data", "width": 80},
	# 	{"label": _("Subscription"), "fieldname": "subscription", "fieldtype": "Link", "options": "Subscription", "width": 150},
	# 	{"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
	# 	{"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
	# 	{"label": _("Invoice Name"), "fieldname": "invoice_name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
	# 	{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
	# 	{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
	# 	{"label": _("Subscription Plan"), "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 150},
	# 	{"label": _("Amount"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
	# 	{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
	# 	{"label": _("Penalty %"), "fieldname": "fine_percent", "fieldtype": "Float", "width": 120},
	# 	{"label": _("Delay Days"), "fieldname": "num_of_delay_days", "fieldtype": "Int", "width": 120},
	# 	{"label": _("Penalty Amount"), "fieldname": "deferred_revenue_amount", "fieldtype": "Currency", "width": 120},
	# 	{"label": _("Total Amount after penalty"), "fieldname": "total_with_fine", "fieldtype": "Currency", "width": 120},
	# 	{"label": _("Penalty Journal"), "fieldname": "journal_entry", "fieldtype": "Link", "options": "Journal Entry", "width": 150},
	# 	{"label": _("Penalty Journal Date"), "fieldname": "journal_entry_date", "fieldtype": "Date", "width": 100},
	# ]
 
	columns = [
		{"label": _("Unit"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
		{"label": _("Area"), "fieldname": "unit_area", "fieldtype": "Data", "width": 80},
  		{"label": _("Invoice Name"), "fieldname": "invoice_name", "fieldtype": "Link", "options": "Sales Invoice", "width": 120},
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
		{"label": _("Due Date"), "fieldname": "due_date", "fieldtype": "Date", "width": 100},
    	{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": _("Subscription"), "fieldname": "subscription", "fieldtype": "Link", "options": "Subscription", "width": 150},
		{"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
		{"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
		{"label": _("Subscription Plan"), "fieldname": "item_name", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": _("Amount"), "fieldname": "total", "fieldtype": "Currency", "width": 120},
		{"label": _("Penalty %"), "fieldname": "fine_percent", "fieldtype": "Float", "width": 120},
		{"label": _("Delay Days"), "fieldname": "num_of_delay_days", "fieldtype": "Int", "width": 120},
		{"label": _("Penalty Amount"), "fieldname": "deferred_revenue_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Total Amount after penalty"), "fieldname": "total_with_fine", "fieldtype": "Currency", "width": 120},
		{"label": _("Penalty Journal"), "fieldname": "journal_entry", "fieldtype": "Link", "options": "Journal Entry", "width": 150},
		{"label": _("Penalty Journal Date"), "fieldname": "journal_entry_date", "fieldtype": "Date", "width": 100},
	]


	filters_conditions = [" 1 = 1 "]
	if filters.get("customer"):
		filters_conditions.append(f"invoice.customer = '{filters.get('customer')}'")
	if filters.get("sales_invoice"):
		filters_conditions.append(f"invoice.name = '{filters.get('sales_invoice')}'")
	if filters.get("subscription_plan"):
		filters_conditions.append(f"item.item_name = '{filters.get('subscription_plan')}'")
	
	filter_condition = " AND ".join(filters_conditions)
	if not filter_condition:
		filter_condition = ""
	# query invoices either conected to subscription or not
	query = f"""
		SELECT
			invoice.name AS invoice_name,
			invoice.status,
			invoice.customer,
			invoice.posting_date,
			invoice.due_date,
			invoice.payment_actual_due_date,
			invoice.total,
			invoice.num_of_delay_days,
			invoice.fine_percent,
			invoice.deferred_revenue_amount,
			(invoice.deferred_revenue_amount + invoice.total) AS total_with_fine,
			item.item_name,
			item.amount,
			item.qty AS unit_area
		FROM
			`tabSales Invoice` AS invoice
		Inner JOIN
			`tabSales Invoice Item` AS item ON item.parent = invoice.name
		WHERE
			{filter_condition} AND invoice.docstatus != 2
	"""

	result = frappe.db.sql(query, as_dict=1)
	
 
	# Get all invoice names in result to fetch related subscription data
	invoice_names = [row['invoice_name'] for row in result]

	# Fetch all Subscription Invoices in one query
	subscription_invoices = frappe.db.sql("""
		SELECT si.invoice, si.parent AS subscription, s.start_date, s.end_date
		FROM `tabSubscription Invoice` AS si
		JOIN `tabSubscription` AS s ON s.name = si.parent
		WHERE si.invoice IN %s
	""", (invoice_names,), as_dict=1)

	# Map subscription data by invoice name for quick access
	subscription_data = {si['invoice']: si for si in subscription_invoices}
	

	# Fetch all Journal Entries and their posting dates, mapping them by invoice name
	journal_entries = frappe.db.sql("""
		SELECT jea.reference_name AS invoice_name, jea.parent AS journal_entry, je.posting_date
		FROM `tabJournal Entry Account` AS jea
		JOIN `tabJournal Entry` AS je ON je.name = jea.parent
		WHERE jea.reference_type = 'Sales Invoice' AND jea.reference_name IN %s
	""", (invoice_names,), as_dict=1)

	journal_entry_data = {je['invoice_name']: je for je in journal_entries}

	for row in result:
		sub_si = subscription_data.get(row['invoice_name'])
		if sub_si:
			row['subscription'] = sub_si['subscription']
			row['start_date'] = sub_si['start_date']
			row['end_date'] = sub_si['end_date']
   
		# Assign journal entry data if available
		je = journal_entry_data.get(row['invoice_name'])
		if je:
			row['journal_entry'] = je['journal_entry']
			row['journal_entry_date'] = je['posting_date']
   
			if row['payment_actual_due_date']:
				row['due_date'] = row['payment_actual_due_date']
			days = date_diff(today(), row['due_date'])
			row['num_of_delay_days'] = max(days, 0)
			row['deferred_revenue_amount'] =  row['fine_percent'] * (row['num_of_delay_days']  or 0) * ( row['total'] or 0)
			row['total_with_fine'] = row['deferred_revenue_amount'] + row['total']
			
	data = result  

	data = frappe.db.sql(query, as_dict=1)
 
	return columns, result