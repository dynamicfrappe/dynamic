# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt
import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1"
    if filters.get("customer"):
        conditions += f" AND si.customer = '{filters.get('customer')}'"
    if filters.get("from_date"):
        conditions += f" AND si.posting_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND si.posting_date <= '{filters.get('to_date')}'"
    if filters.get("sales_person"):
        conditions += f" AND st.sales_person = '{filters.get('sales_person')}'"
    if filters.get("item_code"):
        conditions += f" AND si_item.item_code = '{filters.get('item_code')}'"         
            
    sql_query = f"""
        SELECT 
            si.customer as customer,
            si.posting_date as posting_date,
            st.sales_person as sales_person,
            si_item.item_code as item_code,
            si_item.item_name as item_name,
            si_item.qty as qty,
            si_item.rate as rate,
            si_item.net_rate as net_rate,
            si_item.discount_percentage as discount_percentage,
            si_item.net_amount as net_amount
        FROM
            `tabSales Invoice` si
        LEFT JOIN
            `tabSales Team` st ON si.name = st.parent
        LEFT JOIN
            `tabSales Invoice Item` si_item ON si.name = si_item.parent
        WHERE
            {conditions}
        """
    result = frappe.db.sql(sql_query, as_dict=1)
    return result


def get_columns(filters):
    columns = [
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 300,
        },
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 300,
        },
        {
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 300,
        },
        {
            "fieldname": "item_code",
            "label": _("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 300,
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 300,
        },
        {
            "fieldname": "qty",
            "label": _("Qty"),
            "fieldtype": "Float",
            "width": 300,
        },
        {
            "fieldname": "discount_percentage",
            "label": _("Discount (%)"),
            "fieldtype": "Percent",
            "width": 300,
        },
        {
            "fieldname": "rate",
            "label": _("Rate"),
            "fieldtype": "Currency",
            "options":"currency",
            "width": 300,
        },
        {
            "fieldname": "net_rate",
            "label": _("Net Rate"),
            "fieldtype": "Currency",
            "options":"currency",
            "width": 300,
        },
        {
            "fieldname": "net_amount",
            "label": _("Net Amount"),
            "fieldtype": "Currency",
            "options":"currency",
            "width": 300,
        },
    ]
    return columns

