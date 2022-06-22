from unittest.util import strclass
from dynamic.e_invoice.utils import get_auth_item_details, get_company_configuration
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
    setting = get_company_configuration(invoice.company,invoice.branch_code or "0")
    customer = frappe.get_doc("Customer", invoice.customer)

    # Prepare object
    doc.issuer = frappe._dict({})
    doc.issuer.address = frappe._dict({})

    doc.receiver = frappe._dict({})
    doc.receiver.address = frappe._dict({})

    # Total Initials
    doc.invoiceLines = []
    doc.totalSalesAmount = round_double(0)
    doc.totalDiscountAmount = round_double(0)
    doc.taxTotals = []
    doc.extraDiscountAmount = round_double(0)
    doc.totalItemsDiscountAmount = round_double(0)
    doc.totalAmount = round_double(0)



    # Issuer Details
    doc.issuer.type = company.issuer_type
    doc.issuer.id = clear_str(company.issuer_id or company.tax_id)
    doc.issuer.name = clear_str(company.company_name)
    doc.issuer.address.branchId = setting.branch.branch_code or 0
    doc.issuer.address.country = clear_str(setting.branch.country_code or company.country_code)
    doc.issuer.address.governate = clear_str(setting.branch.governate or company.governate)
    doc.issuer.address.regionCity = clear_str(setting.branch.region_city or company.regioncity)
    doc.issuer.address.street = clear_str(setting.branch.street or company.street)
    doc.issuer.address.buildingNumber = clear_str(setting.branch.building_number or company.buildingnumber)

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


    doc.taxpayerActivityCode = clear_str(invoice.activity_code or setting.branch.activity_code or company.activity_code)
    # Document Type
    doc.documentType = "i"
    if doc.is_return:
        doc.documentType = "c"
    elif doc.is_debit_note:
        doc.documentType = "d"
    else:
        doc.documentType = "i"

    doc.documentTypeVersion = setting.document_version or "0.9"

    invoice_date = parser.parse(
        f"{invoice.posting_date} {invoice.posting_time}")
    doc.dateTimeIssued = invoice_date.strftime("%Y-%m-%dT%H:%M:%SZ")


    doc.internalId = invoice.name


    doc.purchaseOrderReference = invoice.po_no


    for item in invoice.items :
        invoice_line = frappe._dict()
        invoice_line.unitValue = frappe._dict()
        item_config = get_auth_item_details(item.item_code,invoice.company)
        invoice_line.description = clear_str(item.description)
        invoice_line.internalCode = clear_str(item.item_code)
        invoice_line.itemType = clear_str(item_config.item_type or item.item_type) 
        invoice_line.itemCode = clear_str(item_config.item_code or item.itemcode) 
        invoice_line.unitType = clear_str(item_config.uom)
        invoice_line.quantity = round_double(item.qty)

        # Unit Value
        
        qty = item.qty 
        totalTaxableFees = 0
        discount_rate = item.discount_percentage
        base_rate_after_discount = item.base_rate
        base_rate_before_discount = item.base_price_list_rate or item.base_rate
        base_discount_amount = (base_rate_before_discount * discount_rate /100) * qty

        invoice_line.unitValue.currencySold = invoice.currency
        invoice_line.unitValue.amountEGP = round_double(base_rate_before_discount)
        invoice_line.unitValue.currencyExchangeRate = '' if invoice.currency == "EGP" else round_double(invoice.exchange_rate)
        invoice_line.unitValue.amountSold = '' if invoice.currency == "EGP" else round_double(invoice.exchange_rate * base_rate_before_discount)
        
        # Discount
        if base_discount_amount :
            invoice_line.discount = frappe._dict()
            invoice_line.discount.rate = discount_rate
            invoice_line.discount.amount = round_double(base_discount_amount / qty)

        # Taxes 
        if item.item_tax_template :
            tax_template = frappe.get_doc("Item Tax Template",item.item_tax_template)
            for tax in getattr(tax_template,'taxes',[]) :
                    tax_type = tax.tax_type_invoice
                    tax_subtype = tax.tax_sub_type
                    if tax_type and tax_subtype :
                        
                        pass

        # Totals
        invoice_line.salesTotal = round_double(base_rate_before_discount * qty)
        invoice_line.netTotal = round_double(base_rate_after_discount * qty)
        invoice.valueDifference = round_double(0)
        invoice.totalTaxableFees = round_double(totalTaxableFees)
        invoice.itemsDiscount = round_double(base_discount_amount)
        invoice_line.total = round_double(invoice_line.netTotal- base_discount_amount + invoice.totalTaxableFees)


    return doc


def round_double(x=0):
    return abs(round((x or 0), 4))


def clear_str(x=""):
    special_chars = ['\n', '&', ';', '"']
    for sep in special_chars:
        x = str(x or "").replace(sep, '').strip()
    return str(x).strip()
