# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe

def get_data(filters=None):
    query1 = """
        SELECT 
            i.item_code,
            i.item_name,
            pi.posting_date,
            pi.name as purchase_invoice,
            pi.cost_center,
            pi.set_warehouse as warehouse,
            s.name AS supplier,
            pi_item.qty AS qty,
            pi_item.rate AS net_rate,
            (pi_item.qty * pi_item.rate) AS total,
            pi_item.purchase_order as purchase_order,
            pi.status
        FROM 
            `tabPurchase Invoice` pi
        JOIN 
            `tabPurchase Invoice Item` pi_item ON pi.name = pi_item.parent
        JOIN 
            `tabItem` i ON pi_item.item_code = i.item_code
        JOIN 
            `tabSupplier` s ON pi.supplier = s.name
        WHERE 
            pi.docstatus = 1
    """

    # query2 = """
    #     SELECT 
    #         i.item_code,
    #         i.item_name,
    #         po.transaction_date,
    #         po.name as purchase_order,
    #         po.cost_center,
    #         po.set_warehouse as warehouse,
    #         s.name AS supplier,
    #         po_item.qty AS qty,
    #         po_item.rate AS net_rate,
    #         (po_item.qty * po_item.rate) AS total,
    #         po.status
    #     FROM 
    #         `tabPurchase Order` po
    #     JOIN 
    #         `tabPurchase Order Item` po_item ON po.name = po_item.parent
    #     JOIN 
    #         `tabItem` i ON po_item.item_code = i.item_code
    #     JOIN 
    #         `tabSupplier` s ON po.supplier = s.name
    #     WHERE 
    #         po.docstatus = 1
    # """

    conditions1 = []
    # conditions2 = []

    if filters.get("item_code"):
        conditions1.append("i.item_code = %(item_code)s")
        # conditions2.append("i.item_code = %(item_code)s")
    
    if filters.get("supplier"):
        conditions1.append("s.name = %(supplier)s")
        # conditions2.append("s.name = %(supplier)s")
    
    if filters.get("item_group"):
        conditions1.append("i.item_group = %(item_group)s")
        # conditions2.append("i.item_group = %(item_group)s")
    
    if filters.get("cost_center"):
        conditions1.append("pi.cost_center = %(cost_center)s")
        # conditions2.append("po.cost_center = %(cost_center)s")
    
    if filters.get("warehouse"):
        conditions1.append("pi.set_warehouse = %(warehouse)s")
        # conditions2.append("po.set_warehouse = %(warehouse)s")
    
    if filters.get("date_from"):
        conditions1.append("(pi.posting_date >= %(date_from)s)")
        # conditions2.append("(po.transaction_date >= %(date_from)s)")
    
    if filters.get("date_to"):
        conditions1.append("(pi.posting_date <= %(date_to)s)")
        # conditions2.append("(po.transaction_date <= %(date_to)s)")

    if conditions1:
        query1 += " AND " + " AND ".join(conditions1)

    # if conditions2:
    #     query2 += " AND " + " AND ".join(conditions2)

    data1 = frappe.db.sql(query1, filters, as_dict=True)
    # data2 = frappe.db.sql(query2, filters, as_dict=True)

    # return data1 + data2
    return data1


def get_columns():
    return [
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Purchase Invoice",
            "fieldname": "purchase_invoice",
            "fieldtype": "Link",
            "options": "Purchase Invoice",
            "width": 150
        },
        {
            "label": "Purchase Order",
            "fieldname": "purchase_order",
            "fieldtype": "Link",
            "options": "Purchase Order",
            "width": 150
        },
        {
            "label": "Cost Center",
            "fieldname": "cost_center",
            "fieldtype": "Link",
            "options": "Cost Center",
            "width": 150
        },
        {
            "label": "Warehouse",
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150
        },
        {
            "label": "Supplier",
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "label": "Qty",
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "Net Rate",
            "fieldname": "net_rate",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Total",
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        }
    ]

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
