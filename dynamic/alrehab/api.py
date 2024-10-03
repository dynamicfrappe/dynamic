import frappe
from frappe.utils import today, date_diff, flt
from datetime import datetime, date
from frappe import _
from erpnext.accounts.doctype.subscription.subscription import get_subscription_updates
from frappe.utils import getdate

Domains=frappe.get_active_domains()


@frappe.whitelist()
def get_updates_for_report(name):

    invoice = frappe.get_doc("Sales Invoice", name)
    subscription = frappe.db.sql(f"""
        SELECT s.name as name
        FROM `tabSubscription` as s
        Inner join `tabSubscription Invoice` as si
        on s.name = si.parent
        WHERE  si.invoice = '{invoice.name}'
    """, as_dict=True )

    penalty = 0
    if not subscription:
        return
        
    doc = frappe.get_doc("Subscription", subscription[0]['name'])
    penalty = doc.penalty
    frappe.db.set_value('Sales Invoice', name, {'fine_percent': penalty})
    frappe.db.commit()

    existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": "Sales Invoice",
            "reference_name": invoice.name 
        })

    if not existing_journal_entry:

        if invoice.payment_actual_due_date:
            due_date = invoice.payment_actual_due_date
        else:
            due_date = invoice.due_date
                        
        days = date_diff(today(), due_date)
                                
        total = sum( item.get('amount', 0) for item in invoice.get('items', []))
        frappe.db.set_value('Sales Invoice', invoice.name, {'num_of_delay_days': max(days, 0)})
        frappe.db.set_value('Sales Invoice', invoice.name, {'deferred_revenue_amount': total * days * penalty})
        frappe.db.commit()

@frappe.whitelist()
def get_updates(name):

    invoice = frappe.get_doc("Sales Invoice", name)
    subscription = frappe.db.sql(f"""
        SELECT s.name as name
        FROM `tabSubscription` as s
        Inner join `tabSubscription Invoice` as si
        on s.name = si.parent
        WHERE  si.invoice = '{invoice.name}'
    """, as_dict=True )

    penalty = 0
    if not subscription:
        frappe.msgprint("لا يوجد دفعة صيانة لهذه الفاتورة")
        return
        
    doc = frappe.get_doc("Subscription", subscription[0]['name'])
    penalty = doc.penalty
    frappe.db.set_value('Sales Invoice', name, {'fine_percent': penalty})
    frappe.db.commit()

    existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": "Sales Invoice",
            "reference_name": invoice.name 
        })

    if not existing_journal_entry:

        if invoice.payment_actual_due_date:
            due_date = invoice.payment_actual_due_date
        else:
            due_date = invoice.due_date
                        
        days = date_diff(today(), due_date)
                                
        total = sum( item.get('amount', 0) for item in invoice.get('items', []))
        frappe.db.set_value('Sales Invoice', invoice.name, {'num_of_delay_days': max(days, 0)})
        frappe.db.set_value('Sales Invoice', invoice.name, {'deferred_revenue_amount': total * days * penalty})
        frappe.db.commit()
        frappe.msgprint("تم التحديث.")

    else :
        frappe.msgprint("تم انشاء قيد مسبقا بأخر التحديثات.")


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
def create_deferred_revenue_entry(doc_name):
    try:
        invoice = frappe.get_doc("Sales Invoice", doc_name) 
        get_updates(invoice.name)
        # doc.db_set("docstatus", 1, commit=True)
        company = frappe.get_doc('Company', invoice.company)

        deferred_revenue_amount = invoice.deferred_revenue_amount
        if deferred_revenue_amount <= 0 :
            frappe.throw(_("Deferred Revenue Amount must be greater than zero."))

        existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": "Sales Invoice",
            "reference_name": invoice.name 
        })

        if existing_journal_entry:
            frappe.throw(_("Can't create new journal entry! There is a Journal Entry already existed."))

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

        print("journal entry created")
        journal_entry.save()
        print("journal entry saved")
        journal_entry.submit()
        frappe.db.commit()

        return {"name": journal_entry.name}

    except frappe.DoesNotExistError:
        frappe.throw(_("Document {0} of type {1} does not exist.").format(doc_name, doc_type))

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Deferred Revenue Entry")


@frappe.whitelist()
def create_deferred_revenue_entry_group_of_invoices(doc_type, doc_name):
    try:
        doc = frappe.get_doc(doc_type, doc_name) 
        # doc.db_set("docstatus", 1, commit=True)
        for i in doc.invoices:
            invoice = frappe.get_doc("Sales Invoice", i.invoice)
            company = frappe.get_doc('Company', invoice.company)
            get_updates(invoice.name)
            deferred_revenue_amount = invoice.deferred_revenue_amount
            if deferred_revenue_amount <= 0 :
                frappe.throw(_("Deferred Revenue Amount must be greater than zero in Sales Invoice: {1}.").format(invoice.name))

            existing_journal_entry = frappe.db.exists({
                "doctype": "Journal Entry Account",
                "reference_type": "Sales Invoice",
                "reference_name": invoice.name 
            })
            if existing_journal_entry:
                continue

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

            journal_entry.save()
            journal_entry.submit()
            frappe.db.commit()
        
        return True

    except frappe.DoesNotExistError:
        frappe.throw(_("Document {0} of type {1} does not exist.").format(doc_name, doc_type))

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Deferred Revenue Entry")

    

@frappe.whitelist()
def get_date(doc_type):
    doc = frappe.get_doc("Subscription", doc_type)
    if doc.current_invoice_end >= min(date.today(), doc.end_date):
        return True
    return False