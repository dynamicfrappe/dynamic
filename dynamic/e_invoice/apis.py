from base64 import b64encode
import frappe
import requests
import json
from frappe import _



@frappe.whitelist()
def get_company_auth_token(clientID , clientSecret , base_url):
    # base_url = "https://id.preprod.eta.gov.eg"
    method = "/connect/token"
    str_byte = bytes(f"{clientID}:{clientSecret}", 'utf-8')
    auth = b64encode(str_byte).decode("ascii")
    # headers =  {'Authorization': 'application/octet-stream'}
    headers = { 'Authorization' : f'Basic {auth}',
				 'Content-Type': 'application/x-www-form-urlencoded'}
    body = {"grant_type":"client_credentials"}
    response = requests.post(base_url+method,headers=headers,data=body)
    access_token = response.json().get('access_token')
    if not access_token :
        frappe.throw(_("Invalid Client Tax Auth"))
    return response.json().get('access_token')




@frappe.whitelist()
def submit_invoice_api(json_body,access_token,base_url):
    # base_url = "https://id.preprod.eta.gov.eg"
    method = "/api/v1.0/documentsubmissions"
    # headers =  {'Authorization': 'application/octet-stream'}
    headers = { 'Authorization' : f'Bearer {access_token}',
				 'Content-Type': 'application/json'}
    body = json_body
    response = requests.post(base_url+method,headers=headers,data=body)
    # frappe.msgprint(str(response))
    # frappe.msgprint(str(access_token))
    # if response.status_code != 200 :
    #     frappe.msgprint(str(response.status_code))
    #     frappe.throw(str(response.json()))
    return response.json()


@frappe.whitelist()
def document_invoice_api(uuid,access_token,base_url):
    method = f"/api/v1.0/documents/{uuid}/raw"
    headers = { 'Authorization' : f'Bearer {access_token}',
				 'Content-Type': 'application/json'}
    response = requests.get(base_url+method,headers=headers)
    return response.json()