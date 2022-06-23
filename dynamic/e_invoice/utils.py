from base64 import b64encode
from os import access
from erpnext import get_default_company
import frappe
from frappe import _
import requests


@frappe.whitelist()
def get_company_configuration(company=None, branch_code=0):
    if not company:
        company = get_default_company()
    if not company:
        frappe.throw(_("Company is Required"))
    if not frappe.db.exists("E Invoice Configuration", company):
        frappe.throw(_("Please Add Company in E Invoice Configuration"))

    setting = frappe.get_doc("E Invoice Configuration", company)
    company = frappe.get_doc("Company", company)
    config = frappe._dict({})
    config.document_version = "1.0" if setting.environment == "Production" else "0.9"
    config.environment = (setting.environment == "Production")
    config.company_name = setting.company_name or company.company_name
    config.login_url = setting.prod_login_url if setting.environment == "Production" else setting.pre_login_url
    config.system_url = setting.prod_system_api_url if setting.environment == "Production" else setting.pre_system_api_url
    config.client_id = setting.prod_client_id if setting.environment == "Production" else setting.pre_client_id
    config.client_secret = setting.prod_client_secret if setting.environment == "Production" else setting.pre_client_secret
    config.branch = frappe._dict({})
    branch = frappe._dict({})
    if setting.branches and len(setting.branches or []) > 0 :
        exist_branch = [x for x in setting.branches if str(
            x.branch_code) == str(branch_code or 0)]
        if exist_branch and len(exist_branch) > 0:
            branch = frappe.get_doc("Branches" , exist_branch[0].branch) 

    config.branch = frappe._dict({
        "branch_code": branch.branch_code or branch_code or "0",
        "branch_name": branch.branch_name or "Main",
        "activity_code": branch.activity_code or company.activity_code,
        "country_code": branch.country_code or company.country_code,
        "governate": branch.governate or company.governate,
        "region_city": branch.region_city or company.region_city,
        "street": branch.street or company.street,
        "building_number": branch.building_number or company.building_number
    })

    return config


@frappe.whitelist()
def get_auth_item_details(item_code,company=None):
    if not company:
        company = get_default_company()
    item = frappe.get_doc("Item",item_code)
    item_details = frappe._dict()
    if getattr(item,'e_invoice_setting',[]):
        item_config = [x for x in item.e_invoice_setting if x.company == company]
        if item_config :
            item_config = item_config[0]
        
        item_details.item_code = item.itemcode if not item_config else item_config.item_code
        item_details.item_type = item.item_type if not item_config else item_config.item_type
    return item_details


