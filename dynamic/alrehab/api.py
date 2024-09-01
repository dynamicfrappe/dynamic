import frappe
from frappe.utils import today, date_diff, flt
from datetime import datetime
from frappe import _
from erpnext.accounts.doctype.subscription.subscription import get_subscription_updates
from frappe.utils import getdate


# Called on subscription
@frappe.whitelist()
def update_sales_invoice_penalty(sub_id):
    doc = frappe.get_doc("Subscription", sub_id)
    penalty = doc.penalty
    invoices = doc.invoices
    if invoices:
        for i in invoices:
            # invoice = frappe.get_doc("Sales Invoice", i.invoice)
            frappe.db.set_value('Sales Invoice', i.invoice, {'fine_percent': penalty})
            recalculate_due_date_and_amount(i.invoice)


@frappe.whitelist()
def recalculate_due_date_and_amount(doc_name):
    invoice = frappe.get_doc("Sales Invoice", doc_name)
    if invoice.status == "Overdue":
        due_date = invoice.due_date
        days = date_diff(today(), due_date)
                    
        # calc the total items amount
        total = sum( item.get('amount', 0) for item in invoice.get('items', []))

        frappe.db.set_value('Sales Invoice', doc_name, {'num_of_delay_days': max(days, 0)})
        frappe.db.set_value('Sales Invoice', doc_name, {'deferred_revenue_amount': total * days * invoice.fine_percent})

@frappe.whitelist()
def create_deferred_revenue_entry(doc_type, doc_name):
    try:
        doc = frappe.get_doc(doc_type, doc_name) 
        doc.db_set("docstatus", 1, commit=True)
        company = frappe.get_doc('Company', doc.company)

        deferred_revenue_amount = doc.deferred_revenue_amount
        if deferred_revenue_amount <= 0 :
            frappe.throw(_("Deferred Revenue Amount must be greater than zero."))
        
        if doc_type == "Sales Invoice":
            party = doc.customer
        elif doc_type == "Subscription":
            party = doc.party
        

        existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": doc_type,
            "reference_name": doc_name 
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
            'party': party,
            'reference_type': doc.doctype,
            'reference_name': doc.name
        })
        journal_entry.append("accounts",{
            'account': company.credit_account,
            'credit_in_account_currency': deferred_revenue_amount,
            'reference_type': doc.doctype,
            'reference_name': doc.name
        })

        journal_entry.save()
        print(journal_entry.name)
            # frappe.db.set_value()
        journal_entry.submit()
        frappe.db.commit()
        return {"name": journal_entry.name}

    except frappe.DoesNotExistError:
        frappe.throw(_("Document {0} of type {1} does not exist.").format(doc_name, doc_type))

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Deferred Revenue Entry")


@frappe.whitelist()
def set_total(sub_id):
    doc = frappe.get_doc("Subscription", sub_id)
    invoices = doc.invoices
    total = 0.0
    for invoice in invoices:
        
        existing_journal_entry = frappe.db.exists({
            "doctype": "Journal Entry Account",
            "reference_type": "Sales Invoice",
            "reference_name": invoice.invoice 
        })

        if not existing_journal_entry :
            i = frappe.get_doc("Sales Invoice", invoice.invoice)
            total += i.deferred_revenue_amount

    frappe.db.set_value('Subscription', doc.name, {'deferred_revenue_amount': total})

    return {"total": total}
    
