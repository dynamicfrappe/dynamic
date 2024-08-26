import frappe
from frappe.utils import today, date_diff, flt
from datetime import datetime
from frappe import _

# Called on subscription
@frappe.whitelist()
def update_sales_invoice_penalty(sales_invoice, penalty_value):
    
    invoice = frappe.get_doc("Sales Invoice", sales_invoice)
    frappe.db.set_value('Sales Invoice', sales_invoice, {'fine_percent': penalty_value})
    
    recalculate_due_date_and_amount(invoice.name)

    return {"status": "success!"}

# Called on subscription
@frappe.whitelist()
def set_total(sub_id, total):
    doc = frappe.get_doc("Subscription", sub_id)
    frappe.db.set_value('Subscription', doc.name, {'deferred_revenue_amount': total})
    
# Called on sales invoice refreshing
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
        company = frappe.get_doc('Company', doc.company)

        deferred_revenue_amount = doc.deferred_revenue_amount
        if deferred_revenue_amount <= 0 :
            frappe.throw(_("Deferred Revenue Amount must be greater than zero."))

        if doc_type == "Sales Invoice":
            party_type = "Customer"
            party = doc.customer
        elif doc_type == "Subscription":
            party_type = doc.party_type
            party = doc.party


        # je_name = create_journal_entry(company.debit_account, company.credit_account, deferred_revenue_amount, party_type, party)

        je_ref = doc.je_ref
        print(je_ref)
        if not je_ref : 
            je_name = create_journal_entry(company.debit_account, company.credit_account, deferred_revenue_amount, party_type, party)
            frappe.db.set_value(doc_type, doc_name, {'je_ref': je_name})
        else:
            journal_entry = frappe.get_doc("Journal Entry", je_ref)
            if not journal_entry:
                je_name = create_journal_entry(company.debit_account, company.credit_account, deferred_revenue_amount, party_type, party)
                frappe.db.set_value(doc_type, doc_name, {'je_ref': je_name})
            else:
                frappe.throw(_("Can't create new journal entry! There is Journal Entry already existed: {0}").format(doc.je_ref))


        return {"name": je_name}

    except frappe.DoesNotExistError:
        frappe.throw(_("Document {0} of type {1} does not exist.").format(doc_name, doc_type))

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating Deferred Revenue Entry")


def create_journal_entry(debit_account, credit_account, deferred_revenue_amount, party_type, party):
    journal_entry = frappe.new_doc("Journal Entry")
    journal_entry.posting_date = today()
    journal_entry.voucher_type= 'Deferred Revenue'

    journal_entry.append("accounts",{
        'account': debit_account,
        'debit_in_account_currency': deferred_revenue_amount,
        'party_type': party_type,
        'party': party
    })

    journal_entry.append("accounts",{
        'account': credit_account ,
        'credit_in_account_currency': deferred_revenue_amount
    })

    journal_entry.save(ignore_permissions=True)
    frappe.db.commit()

    return journal_entry.name