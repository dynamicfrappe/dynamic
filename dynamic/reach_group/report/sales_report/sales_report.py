# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns()
	return columns, data


def get_data(filters):
	conditions = " 1=1 "
	if filters.get("from_date"):
		conditions += " and sinv.posting_date >= '%s'"%filters.get("from_date")
	if filters.get("to_date"):
		conditions += " and sinv.posting_date <= '%s'"%filters.get("to_date")
	# if filters.get("type"):
	# 	conditions += " and type = '%s'"%filters.get("type")
	# if filters.get("actions"):
	# 	conditions += " and action = '%s'"%filters.get("actions")
	# # if filters.get("customer_type"):
	# # 	conditions += " and customer_type = '%s'"%filters.get("customer_type")
	# if filters.get("branch"):
	# 	conditions += " and branch = '%s'"%filters.get("branch")
	
	# if filters.get("phone_no"):
	# 	conditions += " and phone_no = '%s'"%filters.get("phone_no")

	sql = f"""
	select sinv.*,team.sales_person from `tabSales Invoice` sinv
	LEFT JOIN `tabSales Team`team
	ON team.parent=sinv.name
	WHERE sinv.status NOT IN ('Cancelled','Draft')
    AND {conditions}
	"""
	frappe.errprint(sql)
	result = frappe.db.sql(sql,as_dict=1)
	return result

def get_columns():
	columns = [
		{
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 150
        },
		{
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 150
        },
	    {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 150
        },
	 	{
            "label": _("Customer Group"),
            "fieldname": "customer_group",
            "fieldtype": "Data",
            "width": 150
        },
	{
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Data",
            "width": 150
        },
		{
            "label": _("Price List"),
            "fieldname": "selling_price_list",
            "fieldtype": "Data",
            "width": 150
        },
		{
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 150
        },
		{
            "label": _("Grand Total"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 150
        },
	{
            "label": _("Rounded Total"),
            "fieldname": "rounded_total",
            "fieldtype": "Currency",
            "width": 150
        },
	{
            "label": _("Net Total"),
            "fieldname": "net_total",
            "fieldtype": "Currency",
            "width": 150
        },
	{
            "label": _("Outstanding Amount"),
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 150
        },
		{
            "label": _("Currency"),
            "fieldname": "currency",
            "fieldtype": "Data",
            "width": 150
        },
	{
            "label": _("Is Return"),
            "fieldname": "is_return",
            "fieldtype": "Check",
            "width": 150
        },
	# 	{
    #         "label": _("Phone No"),
    #         "fieldname": "phone_no",
    #         "fieldtype": "Data",
    #         "width": 150
    #     },
	# 	{
    #         "label": _("Branch"),
    #         "fieldname": "branch",
    #         "fieldtype": "Data",
    #         "width": 150
    #     },
	#     {
    #         "label": _("Local Source"),
    #         "fieldname": "local_source",
    #         "fieldtype": "Link",
    #         "options": "Local Source",
    #         "width": 150
    #     },
	#     {
    #         "label": _("Date"),
    #         "fieldname": "date",
    #         "fieldtype": "Date",
    #         "width": 150
    #     },
	#     {
    #         "label": _("Time"),
    #         "fieldname": "time",
    #         "fieldtype": "Time",
    #         "width": 150
    #     },
	# {
    #         "label": _("Created By"),
    #         "fieldname": "create_by",
    #         "fieldtype": "Link",
	#         "options": "User",
    #         "width": 150
    #     },
	]
	return columns