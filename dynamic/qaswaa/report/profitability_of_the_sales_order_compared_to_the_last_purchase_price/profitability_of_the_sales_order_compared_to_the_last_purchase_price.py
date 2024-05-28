import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1"
    
    if filters.get("customer"):
        conditions += f""" AND sd.customer = '{filters.get("customer")}'"""
    if filters.get("sales_order"):
        conditions += f""" AND sd.name = '{filters.get("sales_order")}'"""
    if filters.get("set_warehouse"):
        conditions += f""" AND sd.set_warehouse = '{filters.get("set_warehouse")}'"""
    if filters.get("selling_price_list"):
        conditions += f""" AND sd.selling_price_list = '{filters.get("selling_price_list")}'"""    
    if filters.get("from_date"):
        conditions += f""" AND sd.transaction_date >= date('{filters.get("from_date")}')"""
    if filters.get("to_date"):
        conditions += f""" AND sd.transaction_date <= date('{filters.get("to_date")}')"""
  
    if filters.get("cost_center"):
        conditions += f""" AND sd.cost_center = '{filters.get("cost_center")}'"""
    if filters.get("sales_person"):
        conditions += f""" AND sii_sp.sales_person = '{filters.get("sales_person")}'"""

    sql = f'''
        SELECT 
            sd.name AS sales_order,
            item.item_code,
            item.item_name,
            item.qty,
            item.rate,
            (
                SELECT pii.rate
                FROM `tabPurchase Invoice` pi
                INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
                WHERE pii.item_code = item.item_code
                ORDER BY pi.creation DESC
                LIMIT 1
            ) AS purchase_invoice_rate,
            item.qty * (
                SELECT pii.rate
                FROM `tabPurchase Invoice` pi
                INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
                WHERE pii.item_code = item.item_code
                ORDER BY pi.creation DESC
                LIMIT 1
            ) AS total_purchase,
            item.rate - (
                SELECT pii.rate
                FROM `tabPurchase Invoice` pi
                INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
                WHERE pii.item_code = item.item_code
                ORDER BY pi.creation DESC
                LIMIT 1
            ) AS variance,
            (item.rate - (
                SELECT pii.rate
                FROM `tabPurchase Invoice` pi
                INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
                WHERE pii.item_code = item.item_code
                ORDER BY pi.creation DESC
                LIMIT 1
            )) * item.qty AS total_variance,
            CONCAT(
                ROUND(
                    (
                        (item.rate - (
                            SELECT pii.rate
                            FROM `tabPurchase Invoice` pi
                            INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
                            WHERE pii.item_code = item.item_code
                            ORDER BY pi.creation DESC
                            LIMIT 1
                        )) / (
                            SELECT pii.rate
                            FROM `tabPurchase Invoice` pi
                            INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
                            WHERE pii.item_code = item.item_code
                            ORDER BY pi.creation DESC
                            LIMIT 1
                        ) * 100
                    ),
                    2
                ),
                '%'
            ) AS variance_percentage,
            (
                SELECT sii.rate
                FROM `tabSales Order` si
                INNER JOIN `tabSales Order Item` sii ON sii.parent = si.name
                WHERE sii.item_code = item.item_code
                ORDER BY si.creation DESC
                LIMIT 0,1
            ) AS last_price_1,
            (
                SELECT sii.rate
                FROM `tabSales Order` si
                INNER JOIN `tabSales Order Item` sii ON sii.parent = si.name
                WHERE sii.item_code = item.item_code
                ORDER BY si.creation DESC
                LIMIT 1,1
            ) AS last_price_2,
            (
                SELECT sii.rate
                FROM `tabSales Order` si
                INNER JOIN `tabSales Order Item` sii ON sii.parent = si.name
                WHERE sii.item_code = item.item_code
                ORDER BY si.creation DESC
                LIMIT 2,1
            ) AS last_price_3
        FROM 
            `tabSales Order` sd
        INNER JOIN
            `tabSales Order Item` item ON item.parent = sd.name
        LEFT JOIN
            `tabSales Team` sii_sp ON sd.name = sii_sp.parent 
        WHERE {conditions}
    '''
    data = frappe.db.sql(sql, as_dict=True)

    return data








def get_columns():
    columns = [
        {
            "fieldname": "sales_order",
            "label": _("Sales Order"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 300,
        },
        {
            "fieldname": "item_code",
            "label": _("Item Code"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "item_name",
            "label": _("Item Name"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "qty",
            "label": _("Quantity"),
            "fieldtype": "Float",
            "width": 100
        },
        {
            "fieldname": "rate",
            "label": _("Selling price Rate"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "purchase_invoice_rate",
            "label": _("Purchase Invoice Rate"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_purchase",
            "label": _("Total Purchase"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "variance",
            "label": _("Variance"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "total_variance",
            "label": _("Total Variance"),
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "fieldname": "variance_percentage",
            "label": _("Variance Percentage"),
            "fieldtype": "Percent",
            "width": 100,
        },
        {
            "fieldname": "last_price_1",
            "label": _("Last Price 1"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "last_price_2",
            "label": _("Last Price 2"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "last_price_3",
            "label": _("Last Price 3"),
            "fieldtype": "Currency",
            "width": 100,
        },
    ]
    return columns





