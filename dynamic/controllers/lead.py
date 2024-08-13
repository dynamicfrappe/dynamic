import frappe
from frappe import _
import requests
import json
from dynamic.api_method.auth import get_token
Domains=frappe.get_active_domains()

@frappe.whitelist(allow_guest = True)
def before_validate(self, event):
    if 'Logistics' in Domains :
        if self.transfer :
            set_transfer(self)
            transfer_lead(self)
        if self.lead_owner:
            create_user_permission(self)

def create_user_permission(self):
    if not frappe.db.exists("User Permission", { "user" : self.lead_owner,"for_value": self.name}):
        user_permission = frappe.new_doc("User Permission")
        user_permission.user = self.lead_owner
        user_permission.allow = self.doctype
        user_permission.for_value = self.name
        user_permission.insert()

def transfer_lead(self):
    token = get_token()
    url = f"{token.get('base_url')}/api/resource/Lead"
    print(url)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token.get('token')}"
    }
    print(f"token {token.get('token')}")
    data = {
        "doctype": self.doctype,
        "lead_name": self.lead_name,
        "status": self.status,
        "source": self.source,
        "email_id": self.email_id,
        "phone": self.phone ,
        "transfer_by" : self.transfer_by
    }
    response = requests.post(url, headers=headers , data=json.dumps(data))

    print("*"*40)
    print(response.json())

def set_transfer(self):
    self.transfer_by = f"Transfer By {self.company}"











