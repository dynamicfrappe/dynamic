import frappe
from frappe.utils import flt, getdate

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": "Customer Name",
            "fieldname": "customer_name",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200
        },
        {
            "label": "Customer Mobile Number", 
            "fieldname": "mobile_number", 
            "fieldtype": "Data", 
            "width": 200
        },
        {
            "label": "Last Sales Invoice",
            "fieldname": "last_sales_invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 200
        },
        {
            "label": "Posting Date", 
            "fieldname": "posting_date", 
            "fieldtype": "Date", 
            "width": 200
        },
        {
            "label": "Paid Amount", 
            "fieldname": "paid_amount", 
            "fieldtype": "Currency", 
            "width": 200
        },
    ]

def get_data(filters):
    data = []
    
    conditions = []
    if filters.get("from_date"):
        conditions.append("posting_date >= '{}'".format(filters["from_date"]))
    if filters.get("to_date"):
        conditions.append("posting_date <= '{}'".format(filters["to_date"]))
    if filters.get("customer"):
        conditions.append("customer = '{}'".format(filters["customer"]))

    customer_conditions = " AND ".join(conditions) if conditions else ""

    customers = frappe.get_all('Customer', fields=['name', 'mobile_no'])

    for customer in customers:
        if filters.get("customer") and filters["customer"] != customer.name:
            continue

        invoice_conditions = "customer = '{}' AND is_return = 0 AND docstatus = 1".format(customer.name)
        if customer_conditions:
            invoice_conditions += " AND " + customer_conditions

        invoice = frappe.db.sql("""
            SELECT name, posting_date, grand_total 
            FROM `tabSales Invoice`
            WHERE {}
            ORDER BY posting_date DESC
            LIMIT 1
        """.format(invoice_conditions), as_dict=1)

        if invoice:
            invoice = invoice[0]

            allocated_amounts = frappe.db.sql("""
                SELECT SUM(allocated_amount) 
                FROM `tabPayment Entry Reference` 
                WHERE reference_name = %s
            """, (invoice.name), as_list=1)

            total_allocated_amount = allocated_amounts[0][0] if allocated_amounts[0][0] else 0
            paid_amount = invoice.grand_total - total_allocated_amount

            data.append({
                "customer_name": customer.name,
                "mobile_number": customer.mobile_no,
                "last_sales_invoice": invoice.name,
                "posting_date": invoice.posting_date,
                "paid_amount": paid_amount
            })
        # else:
        #     data.append({
        #         'customer_name': customer.name,
        #         'mobile_number': customer.mobile_no,
        #         'last_sales_invoice': '',
        #         'posting_date': '',
        #         'paid_amount': 0 
        #     })

    return data