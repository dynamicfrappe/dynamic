


import frappe
from frappe import _
from frappe.utils.user import get_users_with_role
from erpnext import get_default_company
DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def alert_cheque_date():
    if "Master Deals" in DOMAINS:
        company = get_default_company()
        get_role= frappe.db.get_value("Company",company,"notification_cheque_role")
        if  (get_role):
            cheque_data = frappe.db.sql("""
            SELECT cheque_no,cheque_date 
            FROM `tabCheque Table` 
            WHERE cheque_date < CURDATE() AND (DATE_ADD(cheque_date, INTERVAL 2 DAY)=CURDATE());
            """,as_dict=1)
            cheque_list = [row['cheque_no'] for row in cheque_data]
            msg = cheque_list
            subject="Cheque Notification"
            print("\n\n\n cheque_list =====> ", cheque_list )
            send_mail_by_role(get_role,msg,subject)

# @frappe.whitelist()
def send_mail_by_role(role,msg,subject):
    try:
        recip_list = get_users_with_role(role)
        if recip_list:
            email_args = {
                "recipients": recip_list,
                "sender": None,
                "subject": subject,
                "message":msg,
                "now": True
            }
            if not frappe.flags.in_test:
                frappe.enqueue(method=frappe.sendmail, queue="short", timeout=500, is_async=True, **email_args)
            else:
                frappe.sendmail(**email_args)
            return email_args
    except Exception as ex:
        print("exception",str(ex))

        
