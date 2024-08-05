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
            transfer_lead(self)


def transfer_lead(self):
    set_transfer(self)
    token = get_token()
    url = f"{token.get('base_url')}/api/resource/Lead"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token.get('token')}"
    }
    data = {
        "doctype": self.doctype,
        "lead_name": self.lead_name,
        "company_name": self.company_name,
        "status": self.status,
        "source": self.source,
        "email_id": self.email_id,
        "phone": self.phone
    }
    response = requests.post(url, headers=headers , data=json.dumps(data))

    print("*"*40)
    print(response.json())

def set_transfer(self):
    self.transfer_by = f"Transfer By{self.company_name}"











