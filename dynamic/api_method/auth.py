import frappe
from frappe import _
import requests

@frappe.whitelist(allow_guest=True)
def login(usr=None, pwd=None):
    """
    Authenticates a user and generates API keys if successful.
    :param usr: Username
    :param pwd: Password
    :return: Authentication result
    """
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.AuthError:
        frappe.clear_messages()
        return {"http_status_code": 401, "message": _("User name or password not valid")}

    api_generate = generate_keys(frappe.session.user)
    if api_generate:
        user = frappe.get_doc('User', frappe.session.user)
        return {
            "http_status_code": 200,
            "api_key": user.api_key,
            "api_secret": api_generate.get("api_secret"),
        }
    else:
        return {"http_status_code": 400, "message": _("Generate Keys Error"), "data": {}}



@frappe.whitelist()
def generate_keys(user):
    """
    Generate API key and secret for the user.
    :param user: Username
    :return: API secret
    """
    user_details = frappe.get_doc("User", user , ignore_permissions=1)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
        user_details.save(ignore_permissions=1)
        frappe.db.commit()

    user_details.api_secret = api_secret
    user_details.save()	
    return {"api_secret": api_secret}


def get_token():
    authentication_doc = frappe.get_single("Authentication Setting")
    token_url = f"{authentication_doc.get('url')}/api/method/dynamic.api_method.auth.login"
    data = {
        "usr" : authentication_doc.user,
        "pwd" : authentication_doc.password
    }
    response = requests.post(token_url, data)
    data = response.json()
    token = f'{data.get("message").get("api_key")}:{data.get("message").get("api_secret")}'
    authentication_doc.db_set("token",token) 
    authentication_doc.save()
    frappe.db.commit()
    print({"token" : authentication_doc.token , "base_url" :authentication_doc.get('url') })
    return {"token" : authentication_doc.token , "base_url" :authentication_doc.get('url') }