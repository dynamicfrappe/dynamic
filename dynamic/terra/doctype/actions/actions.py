# Copyright (c) 2022, Dynamic and contributors
# For license information, please see license.txt
import json
import frappe
from frappe.model.document import Document
Domains=frappe.get_active_domains()

class Actions(Document):
    pass
    def validate(self):
        if 'Logistics' in Domains :
            self.send_notification()

    def send_notification(doc):
        notif_doc = frappe.new_doc('Notification Log')
        notif_doc.subject = f"{doc.doctype} {doc.name} modified by {doc.modified_by}"
        notif_doc.for_user = doc.create_by
        notif_doc.type = "Alert"
        notif_doc.document_type = doc.doctype
        notif_doc.document_name = doc.name
        notif_doc.from_user = frappe.session.user
        notif_doc.insert(ignore_permissions=True)
        
    # def check_permision(self):
    #     if not frappe.db.exists("User Permission", { "user" : self.lead_owner,"for_value": self.name}):
    #         user_permission = frappe.new_doc("User Permission")
    #         user_permission.user = self.lead_owner
    #         user_permission.allow = self.doctype
    #         user_permission.for_value = self.name
    #         user_permission.insert()


@frappe.whitelist()
def get_events(start, end, filters=None):
    from erpnext.controllers.queries import get_match_cond
    from frappe.desk.calendar import get_event_conditions

    filters = json.loads(filters) if filters else {}
    conditions = get_event_conditions("Actions", filters)

    data = frappe.db.sql(
        """
        SELECT
            `tabActions`.name AS name,
            `tabActions`.`from1` AS start,
            `tabActions`.`to` AS end
        FROM
            `tabActions`
        WHERE
            (`tabActions`.`from1` BETWEEN %(start)s AND %(end)s)
            {conditions}
        """.format(conditions=conditions),
        {"start": start, "end": end},
        as_dict=True,
        update={"allDay": 0}
    )
    
    return data

