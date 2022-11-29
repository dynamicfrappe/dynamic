

import frappe
from frappe import _
from frappe.utils import getdate
from datetime import datetime
from frappe.utils.background_jobs import  enqueue
from frappe.model.mapper import get_mapped_doc

DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def opportunity_notifiy(self, *args, **kwargs):
    if "IFI" in DOMAINS:
        get_alert_dict(self)
        #reciever
        email_quotation(self, *args, **kwargs)
        
@frappe.whitelist()
def daily_opportunity_notify(self, *args, **kwargs ):
    # date_now =getdate()
    today = datetime.now().strftime('%Y-%m-%d')
    sql = f"""
        select name,contact_by,customer_name,contact_date,'Opportunity' as doctype from tabOpportunity to2 
		where CAST(contact_date AS DATE) ='{today}'
    """
    data = frappe.db.sql(sql,as_dict=1)
    for opprt in data:
        get_alert_dict(opprt)          

@frappe.whitelist()
def get_alert_dict(self):
    owner_name = self.contact_by
    customer_name = self.customer_name
    contact_date = self.contact_date
    notif_doc = frappe.new_doc('Notification Log')
    notif_doc.subject = f"{owner_name} Contact to {customer_name} at {contact_date}"
    notif_doc.for_user = owner_name
    notif_doc.type = "Mention"
    notif_doc.document_type = self.doctype
    notif_doc.document_name = self.name
    notif_doc.from_user = frappe.session.user
    notif_doc.insert(ignore_permissions=True)




@frappe.whitelist()
def email_quotation(self,*args, **kwargs): 
		receiver = frappe.db.get_value("User", self.contact_by, "email")
		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _("Quotation Appointement"),
				"subject": 'Quotation Appointement At Date'.format(self.contact_date),
                # "message": self.get_message(),
				# "attachments": [frappe.attach_print(self.doctype, self.name, file_name=self.name)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
				}
			enqueue(method=frappe.sendmail, queue="short", timeout=300,now=True, is_async=True,**email_args)
		else:
			frappe.msgprint(_("{0}: Next Contatct By User Has No Mail, hence email not sent").format(self.contact_by))


@frappe.whitelist()
def email_supplier_invoice(self,*args, **kwargs): 
		receiver = frappe.db.get_value("Supplier", self.supplier, "email_id")
		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _("Please GET Notify "),
				"subject": 'Purchase Receipt - IN'.format(self.posting_date),
				# "attachments": [frappe.attach_print(self.doctype, self.name, file_name=self.name)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
				}
			enqueue(method=frappe.sendmail, queue="short", timeout=300,now=True, is_async=True,**email_args)
		else:
			frappe.msgprint(_("{0}: Supplier ha no mail, hence email not sent").format(self.supplier))

@frappe.whitelist()
def create_furniture_installation_order(source_name, target_doc=None):
    doclist = get_mapped_doc("Sales Order", source_name, {
        "Sales Order": {
            "doctype": "Installations Furniture",
            "field_map": {
                "name": "sales_order",
                "customer": "customer"
            },
            "validation": {
                "docstatus": ["=", 1]
            }
        },
        "Sales Order Item": {
            "doctype": "Installation Furniture Item",
            "field_map": {
                "name":"ref_name",
                "item_code": "item_code",
                "item_name": "item_name",
                "qty": "qty",
                "rate": "rate",
                "amount": "amount",
                "delivery_date":"delivery_date",
            }
        }
    }, target_doc)
    
    return doclist
    

# def check_child_table_qty(self,*args, **kwargs):
#     frappe.errprint(f'--{self}->{args}-->>{kwargs}')
#     frappe.errprint(f'--{self.items[0].item_code}')
#     frappe.throw('stop')
#     ...