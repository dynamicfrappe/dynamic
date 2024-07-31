import frappe
from frappe import _

def execute(filters=None):
    data = get_data(filters)
    columns = get_columns(data)
    return columns, data


def get_data(filters):
    query = """
        SELECT 
            mp.type AS mode_of_payment_type,
            a.account_currency AS currency,
            SUM(pe.paid_amount) AS total_paid_amount
        FROM 
            `tabPayment Entry` pe
        JOIN 
            `tabMode of Payment` mp ON pe.mode_of_payment = mp.name
        JOIN 
            `tabMode of Payment Account` mpa ON mp.name = mpa.parent
        JOIN 
            `tabAccount` a ON mpa.default_account = a.name
        WHERE 
            pe.payment_type = 'Receive'
            AND pe.status = 'Submitted'
            AND mp.type = 'Cash'
            AND mp.enabled = '1'
        GROUP BY
            mp.type, a.account_currency
    """
    return frappe.db.sql(query, as_dict=True)


def get_columns(data):
    currencies = set(row['currency'] for row in data)
    columns = [
        {
            "label": f"Type ({currency})",
            "fieldname": f"mode_of_payment_type_{currency}",
            "fieldtype": "Data",
            "width": 150
        }
    ]
    for currency in currencies:
        columns.append({
            "label": f"Total Paid Amount ({currency})",
            "fieldname": f"total_paid_amount_{currency}",
            "fieldtype": "Currency",
            "options": currency,
            "width": 150
        })
    return columns

