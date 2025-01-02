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


def on_update(self, event):
    if 'Logistics' in Domains :
        send_notification(self)

def send_notification(doc):
	notif_doc = frappe.new_doc('Notification Log')
	notif_doc.subject = f"{doc.doctype} {doc.name} modified by {doc.modified_by}"
	notif_doc.for_user = doc.lead_owner
	notif_doc.type = "Alert"
	notif_doc.document_type = doc.doctype
	notif_doc.document_name = doc.name
	notif_doc.from_user = frappe.session.user
	notif_doc.insert(ignore_permissions=True)

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
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"token {token.get('token')}"
    }
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

    print(response.json())

def set_transfer(self):
    self.transfer_by = f"Transfer By {self.company}"











