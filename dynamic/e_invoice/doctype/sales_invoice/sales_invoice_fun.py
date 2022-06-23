from unittest.util import strclass
from dynamic.e_invoice.apis import get_company_auth_token, submit_invoice_api
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
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    company = frappe.get_doc("Company", invoice.company)
    setting = get_company_configuration(invoice.company,invoice.branch_code or "0")
    customer = frappe.get_doc("Customer", invoice.customer)
    invoice_json = get_invoice_json(invoice,company,setting,customer)
    result.documents.append(invoice_json)
    result = json.dumps(result)
    if setting.document_version == "0.9" :
        access_token = get_company_auth_token(setting.client_id,setting.client_secret,setting.login_url)
        submit_response = submit_invoice_api(result,access_token,setting.system_url)
        frappe.msgprint (str(submit_response))
    return result
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

@frappe.whitelist()
def update_invoice_submission_status(submit_response):
    # Update All Invoices With Submission Status
    """
    "Submitted" for accepted Docs
    "Invalid" for Rejected Docs
    """
    pass
def get_invoice_json(invoice , company , setting , customer ):
    """
    get single invoice json
    """
    doc = frappe._dict({})


    doc.internalID = invoice.name

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


    # doc.purchaseOrderReference = invoice.po_no

    totalTaxes = 0
    for item in invoice.items :
        invoice_line = frappe._dict()
        invoice_line.unitValue = frappe._dict()
        item_config = get_auth_item_details(item.item_code,invoice.company)
        invoice_line.description = clear_str(item.description)
        invoice_line.internalCode = clear_str(item.item_code)
        invoice_line.itemType = clear_str(item_config.item_type or item.item_type) 
        invoice_line.itemCode = clear_str(item_config.item_code or item.itemcode) 
        invoice_line.unitType = clear_str(item.uom)
        # frappe.msgprint(invoice_line.unitType)
        invoice_line.quantity = round_double(item.qty)
        
        # Unit Value
        
        qty = item.qty 
        totalTaxableFees = 0
        discount_rate = max(item.discount_percentage,0)
        base_rate_after_discount = item.base_rate
        base_rate_before_discount = item.base_price_list_rate or item.base_rate
        base_discount_amount = (base_rate_before_discount * discount_rate /100) * qty
        invoice_line.unitValue.currencySold = invoice.currency
        invoice_line.unitValue.amountEGP = round_double(base_rate_before_discount)
        invoice_line.unitValue.currencyExchangeRate = 0 if invoice.currency == "EGP" else round_double(invoice.exchange_rate)
        invoice_line.unitValue.amountSold = 0 if invoice.currency == "EGP" else round_double(invoice.exchange_rate * base_rate_before_discount)
        
        
        # Discount
        if base_discount_amount :
            invoice_line.discount = frappe._dict()
            invoice_line.discount.rate = discount_rate
            invoice_line.discount.amount = round_double(base_discount_amount / qty)

        # Taxes 
        invoice_line.taxableItems = []
        if item.item_tax_template :
            tax_template = frappe.get_doc("Item Tax Template",item.item_tax_template)
            for tax in getattr(tax_template,'taxes',[]) :
                    tax_type = tax.tax_type_invoice
                    tax_subtype = tax.tax_sub_type
                    if tax_type and tax_subtype :
                        tax_type_code,taxable = frappe.db.get_value("Tax Types",tax_type,['code','taxable'])
                        tax_subtype_code,fixed_amount = frappe.db.get_value("Tax Types",tax_subtype,['code','fixed_amount'])
                        tax_row = frappe._dict()
                        tax_row.taxType = tax_type_code
                        tax_row.subType = tax_subtype_code
                        tax_row.rate = round_double(0 if fixed_amount else tax.tax_rate)

                        row_tax = tax.amount if fixed_amount else ( base_rate_after_discount * tax.tax_rate/100)
                        row_tax_toal = row_tax * qty
                        tax_row.amount = round_double(row_tax_toal)
                        invoice_line.taxableItems.append(tax_row)
                        if taxable :
                            totalTaxableFees += row_tax_toal
                            totalTaxes += row_tax_toal
                        # Add Tax to Tax Totals
                        exist = 0
                        for prevTax in doc.taxTotals :
                            if prevTax.taxType == tax_row.taxType :
                                prevTax.amount += round_double(tax_row.amount)
                                exist = 1
                                break
                        if not exist :
                            doc.taxTotals.append(frappe._dict({
                                "taxType":tax_row.taxType,
                                "amount":tax_row.amount,
                            }))



        # Line Totals
        invoice_line.salesTotal = round_double(base_rate_before_discount * qty)
        invoice_line.netTotal = round_double(base_rate_after_discount * qty)
        invoice_line.valueDifference = round_double(0)
        invoice_line.totalTaxableFees = round_double(0)
        invoice_line.itemsDiscount = round_double(base_discount_amount)
        invoice_line.total = round_double(invoice_line.netTotal + totalTaxableFees)
        
        
        doc.invoiceLines.append(invoice_line)
    
    doc.totalSalesAmount = round_double(sum([x.salesTotal for x in doc.invoiceLines]))
    doc.netAmount = round_double(sum([x.netTotal for x in doc.invoiceLines]))
    doc.totalDiscountAmount = round_double(sum([x.itemsDiscount for x in doc.invoiceLines]))
    doc.extraDiscountAmount = round_double((invoice.discount_amount or 0) * (doc.exchange_rate or 1))
    doc.totalItemsDiscountAmount = round_double(doc.totalDiscountAmount + doc.extraDiscountAmount)
    totalAmount = sum([x.total for x in doc.invoiceLines])
    doc.totalAmount = round_double(totalAmount - doc.extraDiscountAmount)


    return doc


def round_double(x=0):
    return abs(round((x or 0), 4))


def clear_str(x=""):
    special_chars = ['\n', '&', ';', '"']
    for sep in special_chars:
        x = str(x or "").replace(sep, '').strip()
    return str(x).strip()
