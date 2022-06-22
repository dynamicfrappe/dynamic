from unittest.util import strclass
import frappe
import json
import requests
from datetime import datetime, time, timedelta, date
from dateutil import parser


@frappe.whitelist()
def post_sales_invoice(invoice_name):
    # try:
    result = frappe._dict({"documents": []})
    invoice_json = get_invoice_json(invoice_name)
    result.documents.append(invoice_json)
    return json.dumps(result)
    ########## get server url ############
    server_url = frappe.db.get_single_value('EInvoice Setting', 'url')
    # if not server_url:
    #    frappe.throw("You Must Enter Server Url in E Invoice Setting")
    api_url = "/api/recive_invoice_data"
    full_url = str(server_url)+str(api_url)
    r = requests.post(
        full_url,
        data=json.dumps(result)
    )
    if r.status_code == 200:
        print("200 from if")
        sql = """update `tabSales Invoice` set is_send=1 where name='%s'""" % invoice_name
        print("sqlllllllllllllll", sql)
        frappe.db.sql(
            """update `tabSales Invoice` set is_send=1 where name='%s'""" % invoice_name)
        frappe.db.commit()
        frappe.msgprint("Invoice Send Successfully")
    else:
        frappe.msgprint("Failed To Send Invoice")
    # except Exception as e:
    #     frappe.local.response["message"] = str(e)
    #     frappe.local.response['http_status_code'] = 400


def get_invoice_json(invoice_name):
    """
    get single invoice json
    """
    doc = frappe._dict({})
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    company = frappe.get_doc("Company", invoice.company)
    customer = frappe.get_doc("Customer", invoice.customer)
    # Prepare object
    doc.invoiceLines = []
    doc.issuer = frappe._dict({})
    doc.issuer.address = frappe._dict({})

    doc.receiver = frappe._dict({})
    doc.receiver.address = frappe._dict({})

    # Issuer Details
    doc.issuer.type = company.issuer_type
    doc.issuer.id = clear_str(company.issuer_id or company.tax_id)
    doc.issuer.name = clear_str(company.company_name)
    doc.issuer.address.branchId = 0
    doc.issuer.address.country = clear_str(company.country_code)
    doc.issuer.address.governate = clear_str(company.governate)
    doc.issuer.address.regionCity = clear_str(company.regioncity)
    doc.issuer.address.street = clear_str(company.street)
    doc.issuer.address.buildingNumber = clear_str(company.buildingnumber)

    # Receiver Details
    doc.receiver.type = customer.receiver_type
    doc.receiver.id = clear_str(customer.receiver_id or customer.tax_id)
    doc.receiver.name = clear_str(customer.customer_name)
    doc.receiver.address.branchId = clear_str(customer.branchid)
    doc.receiver.address.country = clear_str(customer.country_code)
    doc.receiver.address.governate = clear_str(customer.governate)
    doc.receiver.address.regionCity = clear_str(customer.regioncity)
    doc.receiver.address.street = clear_str(customer.street)
    doc.receiver.address.buildingNumber = clear_str(customer.buildingnumber)

    # Document Type
    doc.documentType = "i"
    if doc.is_return:
        doc.documentType = "c"
    elif doc.is_debit_note:
        doc.documentType = "d"
    else:
        doc.documentType = "i"

    doc.documentTypeVersion = "0.9"

    invoice_date = parser.parse(
        f"{invoice.posting_date} {invoice.posting_time}")
    doc.dateTimeIssued = invoice_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    doc.taxpayerActivityCode = invoice.activity_code or company.activity_code

    return doc


def round_double(x=0):
    return abs(round((x or 0), 4))


def clear_str(x=""):
    special_chars = ['\n', '&', ';', '"']
    for sep in special_chars:
        x = str(x or "").replace(sep, '').strip()
    return str(x).strip()
