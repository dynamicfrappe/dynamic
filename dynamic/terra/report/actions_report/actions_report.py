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
	conditions = " where 1=1 "
	if filters.get("from"):
		conditions += " and from1 >= '%s'"%filters.get("from")
	if filters.get("to"):
		conditions += " and `to` <= '%s'"%filters.get("to")
	if filters.get("type"):
		conditions += " and type = '%s'"%filters.get("type")
	if filters.get("actions"):
		conditions += " and action = '%s'"%filters.get("actions")
	if filters.get("document_type"):
		conditions += " and document_type = '%s'"%filters.get("document_type")
	if filters.get("branch"):
		conditions += ' and branch = "%s"'%filters.get("branch")
	
	if filters.get("phone_no"):
		conditions += " and phone_no = '%s'"%filters.get("phone_no")

	sql = f"""
	select * from `tabActions`
		{conditions} 
	"""
	result = frappe.db.sql(sql,as_dict=1)
	return result

def get_columns():
	columns = [
		{
            "label": _("Type"),
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 150
        },
	    {
            "label": _("Action Name"),
            "fieldname": "action_name",
            "fieldtype": "Data",
            "width": 150
        },
	{
            "label": _("Action Type"),
            "fieldname": "action_type",
            "fieldtype": "Data",
            "width": 150
        },
		{
            "label": _("Description"),
            "fieldname": "description",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Document Type"),
            "fieldname": "document_type",
            "fieldtype": "Link",
            "options": "DocType", 
            "width": 150
        },
        {
            "label": _("Document Name"),
            "fieldname": "document_name",
            "fieldtype": "Dynamic Link",
            "options": "document_type", 
            "width": 150
        },
		{
            "label": _("Phone No"),
            "fieldname": "phone_no",
            "fieldtype": "Data",
            "width": 150
        },
		{
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Data",
            "width": 150
        },
	    {
            "label": _("Local Source"),
            "fieldname": "local_source",
            "fieldtype": "Link",
            "options": "Local Source",
            "width": 150
        },
	    {
            "label": _("From"),
            "fieldname": "date",
            "fieldtype": "Datetime",
            "width": 150
        },
	    {
            "label": _("To"),
            "fieldname": "to",
            "fieldtype": "Datetime",
            "width": 150
        },
	{
            "label": _("Created By"),
            "fieldname": "create_by",
            "fieldtype": "Link",
	        "options": "User",
            "width": 150
        },
	]
	return columns