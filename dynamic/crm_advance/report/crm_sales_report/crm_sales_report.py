# Copyright (c) 2025, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate

def execute(filters=None):
    columns = [
        {
            "label": "Person Name", 
            "fieldname": "person_name", 
            "fieldtype": "link", 
            "width": 300
        },
        {
            "label": "Mobile_No",
            "fieldname": "Mobile_No",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Status", 
            "fieldname": "status", 
            "fieldtype": "Data", 
            "width": 200
        },
        {
            "label": "Sales Person", 
            "fieldname": "sales_person", 
            "fieldtype": "Data", 
            "width": 300
        },
        {
            "label": "Lead Owner", 
            "fieldname": "lead_owner", 
            "fieldtype": "Data", 
            "width": 300
        },
        {
            "label": "Comments", 
            "fieldname": "notes", 
            "fieldtype": "data", 
            "width": 300
        },
    ]
    
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    status = filters.get("status")
    sales_person = filters.get("sales_person")
    Mobile_No=filters.get("Mobile_No")

    if start_date:
        start_date = getdate(start_date)
    if end_date:
        end_date = getdate(end_date)
    
    filters_dict = {}

    if start_date and not end_date:
        filters_dict['creation'] = ['>=', start_date]  
    if end_date and not start_date:
        filters_dict['creation'] = ['<=', end_date]  
    if start_date and end_date:
        filters_dict['creation'] = ['between', [start_date, end_date]] 

    if status != "all":
        filters_dict['status'] = status
    
    
    if sales_person:
        filters_dict['sales_person'] = sales_person
    
    if Mobile_No:
        filters_dict['Mobile_No']=['like',f"%{Mobile_No}%"]

    data = frappe.get_all(
        'Lead',
        fields=['name', 'lead_name as person_name', 'status', 'sales_person', 'lead_owner', 'creation', 'Mobile_No','notes'],
        filters=filters_dict
    )
    
    return columns, data
