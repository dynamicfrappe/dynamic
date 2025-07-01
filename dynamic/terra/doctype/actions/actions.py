# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Actions(Document):
    pass
def send_emails(doc, method=None):

    frappe.get_doc({
        "doctype": "Notification Log",
        "subject": f"New actions has added : {doc.name}",
        "for_user": doc.email,  
        "type": "Alert",
        "document_type": doc.doctype,
        "document_name": doc.name
    }).insert(ignore_permissions=True)    


