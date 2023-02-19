import frappe
from frappe.model.mapper import get_mapped_doc

from werkzeug.wrappers import Response

import json

def elevana_lead_before_insert(doc,fun=''):
    set_sales_person(doc)


def set_sales_person(doc):
    # frappe.msgprint('ss')
    if not doc.sales_person :
        employee = frappe.db.get_value("Employee" , {'user_id':frappe.session.user} , 'name')
        if employee :
            sales_person = emp = frappe.db.get_value("Sales Person" , {'employee':employee} , 'name')
            if sales_person :
                doc.sales_person = sales_person


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
    def set_missing_values(source, target):
        _set_missing_values(source, target)

    target_doc = get_mapped_doc(
        "Lead",
        source_name,
        {"Lead": {"doctype": "Quotation", "field_map": {"name": "party_name"}}},
        target_doc,
        set_missing_values,
    )
    target_doc.quotation_to = "Lead"
    target_doc.run_method("set_missing_values")
    target_doc.run_method("set_other_charges")
    target_doc.run_method("calculate_taxes_and_totals")

    return target_doc


def _set_missing_values(source, target):
    address = frappe.get_all(
        "Dynamic Link",
        {
            "link_doctype": source.doctype,
            "link_name": source.name,
            "parenttype": "Address",
        },
        ["parent"],
        limit=1,
    )

    contact = frappe.get_all(
        "Dynamic Link",
        {
            "link_doctype": source.doctype,
            "link_name": source.name,
            "parenttype": "Contact",
        },
        ["parent"],
        limit=1,
    )

    if address:
        target.customer_address = address[0].parent

    if contact:
        target.contact_person = contact[0].parent

    if getattr(source, 'sales_person', None):
        target.set('sales_team', [])
        target.append('sales_team', {
            "sales_person": getattr(source, 'sales_person', None),
            "allocated_percentage": "100",
            # "incentives":"150"
        })


        #dynamic.dynamic.elevana.api.get_customer_name
@frappe.whitelist(allow_guest =1)
def get_customer_name (*args , **kwargs)  :
    #get data 
    data = False
    respone = Response()
    try :
        data =json.loads(frappe.request.data)
    except Exception as e :
        frappe.local.response['message'] = f"Error Accourd   {e}"
        frappe.local.response['http_status_code'] = 400 

    if data :
        #check phone number 
        if not data.get("phone"):
            # frappe.local.response['message'] = "Customer name required"
            # frappe.local.response['http_status_code'] = 400 
            respone.data = "error!"
            return
        sql = frappe.db.sql(f""" SELECT link_title FROM 
            `tabDynamic Link` WHERE parent in  (SELECT parent From `tabContact Phone` WHERE phone =  "{data.get('phone')}" ) """ ,as_dict =1)
        if sql and len(sql) > 0:
            respone.data = str(sql[-1].get("link_title"))
            return respone
