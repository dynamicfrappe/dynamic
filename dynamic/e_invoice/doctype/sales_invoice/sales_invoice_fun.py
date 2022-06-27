from unittest.util import strclass
from dynamic.e_invoice.apis import get_company_auth_token, submit_invoice_api, document_invoice_api
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
    # result = json.dumps(result)
    if setting.document_version == "0.9" :

        access_token = get_company_auth_token(setting.client_id,setting.client_secret,setting.login_url)
        submit_response = submit_invoice_api(json.dumps(result),access_token,setting.system_url)

        # frappe.msgprint(str(json.dumps(result)))
        update_invoice_submission_status(submit_response)
    # frappe.msgprint(str(result))
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
def get_document_sales_invoice(invoice_name):
    # try:
    result = frappe._dict({"documents": []})
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    setting = get_company_configuration(invoice.company,invoice.branch_code or "0")
    access_token = get_company_auth_token(setting.client_id,setting.client_secret,setting.login_url)
    document_response = document_invoice_api(invoice.uuid,access_token,setting.system_url)
    
    
    if document_response.get('status') != 'Invalid':
        invoice.invoice_status = document_response.get('status')
        invoice.uuid = document_response.get('uuid')
    else:
        validationSteps = document_response.get("validationResults")['validationSteps']
        for err in validationSteps:
            if err['error']:
                invoice.error_code += err['error']['errorCode']
                invoice.error_details += err['error']['error']
                err_list = err['error']['innerError']
                if err_list:
                    for index in range(len(err_list)):
                        for k,v in err_list[index].items():
                            invoice.error_details += f'-- {k} :{v}'

        invoice.invoice_status = document_response.get('status')
        
    invoice.save()
    return result

@frappe.whitelist()
def update_invoice_submission_status(submit_response):
    # Update All Invoices With Submission Status
    """
    "Submitted" for accepted Docs
    "Invalid" for Rejected Docs
    """
    if type(submit_response) is str :
        submit_response = json.loads(str(submit_response))
    for accepted_doc in  (submit_response.get("acceptedDocuments") or []):
        internalID = accepted_doc['internalId']
        sinv_doc = frappe.get_doc('Sales Invoice',internalID)
        sinv_doc.uuid = accepted_doc['uuid']
        sinv_doc.long_id = accepted_doc['longId']
        sinv_doc.submission_id = submit_response['submissionId']
        sinv_doc.invoice_status = 'Submitted'
        sinv_doc.error_code = ''
        sinv_doc.error_details = ''
        sinv_doc.save()
        frappe.msgprint(str(sinv_doc.uuid))
        if sinv_doc.uuid :
            get_document_sales_invoice(sinv_doc.name)
        


    for rejected_doc in  (submit_response.get("rejectedDocuments") or []):
        internalID = rejected_doc['internalId']
        sinv_doc = frappe.get_doc('Sales Invoice',internalID)
        sinv_doc.error_code = rejected_doc['error']['code']
        sinv_doc.submission_id = submit_response.get('submissionId', '')
        sinv_doc.invoice_status = 'Invalid'
        err_list = rejected_doc['error']['details']
        err_details = ''
        for index in range(len(err_list)):
            for key,val in err_list[index].items():
                err_details += f'{key} : {err_list[index][key]} --  '        
        sinv_doc.error_details = err_details
        sinv_doc.save()

        
        


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
        invoice_line.totalTaxableFees = 0
        discount_rate = max(item.discount_percentage,0)
        base_rate_after_discount = item.base_rate
        base_discount_amount = (item.discount_amount  * invoice.conversion_rate)
        base_rate_before_discount = base_rate_after_discount + (base_discount_amount / qty)
        # base_discount_amount = (base_rate_before_discount * discount_rate /100) * qty
        invoice_line.unitValue.currencySold = invoice.currency
        invoice_line.unitValue.amountEGP = round_double(base_rate_before_discount)
        invoice_line.unitValue.currencyExchangeRate = 0 if invoice.currency == "EGP" else round_double(invoice.conversion_rate)
        invoice_line.unitValue.amountSold = 0 if invoice.currency == "EGP" else round_double(invoice.conversion_rate * base_rate_before_discount)
        

        # Discount
        if base_discount_amount :
            invoice_line.discount = frappe._dict()
            invoice_line.discount.rate = round_double(0) # discount_rate
            invoice_line.discount.amount = round_double(base_discount_amount)

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

                        row_tax = tax.amount if fixed_amount else ( (base_rate_after_discount + (invoice_line.totalTaxableFees / qty)) * tax.tax_rate/100) 
                        
                        row_tax_toal = row_tax * qty if tax_subtype_code not in ["ST02"] else row_tax

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
                        if fixed_amount and taxable :
                            invoice_line.totalTaxableFees += tax_row.amount



        # Line Totals
        invoice_line.salesTotal = round_double(base_rate_before_discount * qty)
        invoice_line.netTotal = round_double(base_rate_after_discount * qty)
        invoice_line.valueDifference = round_double(0)
        invoice_line.totalTaxableFees = round_double(invoice_line.totalTaxableFees)
        invoice_line.itemsDiscount = round_double(0)
        invoice_line.total = round_double(invoice_line.netTotal + totalTaxableFees)
        
        
        doc.invoiceLines.append(invoice_line)
    
    doc.totalSalesAmount = round_double(sum([x.salesTotal for x in doc.invoiceLines]))
    doc.netAmount = round_double(sum([x.netTotal for x in doc.invoiceLines]))
    doc.totalDiscountAmount = round_double(sum([x.discount.amount for x in doc.invoiceLines if x.discount]))
    doc.extraDiscountAmount = round_double((invoice.discount_amount or 0) * (invoice.conversion_rate or 1))
    doc.totalItemsDiscountAmount = round_double(0)
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
