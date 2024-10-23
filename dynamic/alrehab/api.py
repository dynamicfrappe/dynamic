import frappe
from frappe.utils import today, date_diff, flt
from datetime import datetime, date
from frappe import _
from erpnext.accounts.doctype.subscription.subscription import get_subscription_updates
from frappe.utils import getdate
import json

Domains=frappe.get_active_domains()

# This method is to get the latest state of the invoices
@frappe.whitelist()
def get_updates(name):
    invoice = frappe.get_doc("Sales Invoice", name)
    # Check if there is a subscription for the invoice
    subscription = frappe.db.sql(f"""
        SELECT s.name as name
        FROM `tabSubscription` as s
        Inner join `tabSubscription Invoice` as si
        on s.name = si.parent
        WHERE  si.invoice = '{invoice.name}'
    """, as_dict=True )

    penalty = 0
    if not subscription:
        # if the subscription is not there then fetch the penalty from the invoice
        penalty = invoice.fine_percent
    else:
        # if the subscription is there then fetch the penalty from the subscription
        doc = frappe.get_doc("Subscription", subscription[0]['name'])
        penalty = doc.penalty
        frappe.db.set_value('Sales Invoice', name, {'fine_percent': penalty})
        frappe.db.commit()

    existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": "Sales Invoice",
            "reference_name": invoice.name 
        })
    
    # check if there is a journal entry for the invoice before updating
    if not existing_journal_entry:
        if invoice.payment_actual_due_date:
            due_date = invoice.payment_actual_due_date
        else:
            due_date = invoice.due_date
                        
        days = date_diff(today(), due_date)
                                
        total = sum( item.get('amount', 0) for item in invoice.get('items', []))
        frappe.db.set_value('Sales Invoice', invoice.name, {'num_of_delay_days': max(days, 0)})
        frappe.db.set_value('Sales Invoice', invoice.name, {'deferred_revenue_amount': total * max(days, 0) * penalty})
        frappe.db.commit()
        frappe.msgprint("تم التحديث.")

    else :
        frappe.msgprint("تم انشاء قيد مسبقا بأخر التحديثات.")


@frappe.whitelist()
def create_deferred_revenue_entry(doc_name):
    try:
        invoice = frappe.get_doc("Sales Invoice", doc_name) 
        company = frappe.get_doc('Company', invoice.company)
        get_updates(invoice.name)

        deferred_revenue_amount = invoice.deferred_revenue_amount
        if deferred_revenue_amount <= 0 :
            return {"Done"}

        existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": "Sales Invoice",
            "reference_name": invoice.name 
        })
        if existing_journal_entry:
            return {"Done"}
        
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.posting_date = today()
        journal_entry.voucher_type = 'Deferred Revenue'
        journal_entry.append("accounts",{
            'account': company.debit_account,
            'debit_in_account_currency': deferred_revenue_amount,
            'party_type': "Customer",
            'party': invoice.customer,
            'reference_type': "Sales Invoice",
            'reference_name': invoice.name
        })
        journal_entry.append("accounts",{
            'account': company.credit_account,
            'credit_in_account_currency': deferred_revenue_amount
        })

        # print("journal entry created")
        journal_entry.save()
        journal_entry.submit()
        frappe.db.commit()
        return {"name": journal_entry.name}

    except frappe.DoesNotExistError:
        frappe.throw(_("Document {0} of type {1} does not exist.").format(doc_name, doc_type))

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Deferred Revenue Entry")


@frappe.whitelist()
def create_deferred_revenue_entry_group_of_invoices(invoices):
    try:     
        # Convert the incoming JSON string to a Python list
        invoices = json.loads(invoices)   
        for i in invoices:
            print(i.get('invoice'))
            create_deferred_revenue_entry(i.get('invoice'))
        
        return {"message": "done"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Deferred Revenue Entry")



@frappe.whitelist()
def set_total(sub_id):
    doc = frappe.get_doc("Subscription", sub_id)
    invoices = doc.invoices
    total = 0.0
    for invoice in invoices:
        i = frappe.get_doc("Sales Invoice", invoice.invoice)
        total += i.deferred_revenue_amount
    if doc.deferred_revenue_amount != total:
        frappe.db.set_value('Subscription', doc.name, {'deferred_revenue_amount': total})
        frappe.db.commit()

    return {"total": total}


@frappe.whitelist()
def get_date(doc_type):
    doc = frappe.get_doc("Subscription", doc_type)
    if doc.current_invoice_end >= min(date.today(), doc.end_date):
        return True
    return False