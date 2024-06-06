import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_data(filters):
    conditions = "1=1"
    if filters.get("supplier"):
        conditions += f" AND pi.supplier = '{filters.get('supplier')}'"
    if filters.get("cost_center"):
        conditions += f" AND pi.cost_center = '{filters.get('cost_center')}'"
    if filters.get("purchase_invoice"):
        conditions += f" AND pi.name = '{filters.get('purchase_invoice')}'"        
    if filters.get("from_date"):
        conditions += f" AND pi.posting_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND pi.posting_date <= '{filters.get('to_date')}'"
    if filters.get("item_code"):
        conditions += f" AND pii1.item_code = '{filters.get('item_code')}'"
    if filters.get("item_group"):
        conditions += f" AND pii1.item_group = '{filters.get('item_group')}'"    
    if filters.get("warehouse"):
        conditions += f" AND pii1.warehouse = '{filters.get('warehouse')}'"    

    sql = f'''
        SELECT
            pii1.item_code,
            pii1.item_name,
            (
                SELECT pii_last.rate
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 0,1
            ) AS last_price_1,
            (
                SELECT pi_last.posting_date
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 0,1
            ) AS posting_date_1,
            (
                SELECT pii_last.rate
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 1,1
            ) AS last_price_2,
            (
                SELECT pi_last.posting_date
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 1,1
            ) AS posting_date_2,
            (
                SELECT pii_last.rate
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 2,1
            ) AS last_price_3,
            (
                SELECT pi_last.posting_date
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 2,1
            ) AS posting_date_3,
            (
                SELECT pii_last.rate
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 3,1
            ) AS last_price_4,
            (
                SELECT pi_last.posting_date
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 3,1
            ) AS posting_date_4,
            (
                SELECT pii_last.rate
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 4,1
            ) AS last_price_5,
            (
                SELECT pi_last.posting_date
                FROM `tabPurchase Invoice` pi_last
                INNER JOIN `tabPurchase Invoice Item` pii_last ON pii_last.parent = pi_last.name
                WHERE pii_last.item_code = pii1.item_code
                ORDER BY pi_last.creation DESC
                LIMIT 4,1
            ) AS posting_date_5
        FROM 
            `tabPurchase Invoice` pi
        INNER JOIN
            `tabPurchase Invoice Item` pii1 ON pii1.parent = pi.name
        WHERE {conditions}
    '''

    data = frappe.db.sql(sql, as_dict=True)

    return data



def get_columns():
    columns = [
        # {
        #     "fieldname": "purchase_invoice",
        #     "label": _("Purchase Invoice"),
        #     "fieldtype": "Link",
        #     "options": "Purchase Invoice",
        #     "width": 300,
        # },
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
            "fieldname": "last_price_1",
            "label": _("Last Price 1"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "posting_date_1",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "last_price_2",
            "label": _("Last Price 2"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "posting_date_2",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "last_price_3",
            "label": _("Last Price 3"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "posting_date_3",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "last_price_4",
            "label": _("Last Price 4"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "posting_date_4",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "fieldname": "last_price_5",
            "label": _("Last Price 5"),
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "fieldname": "posting_date_5",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100,
        },
    ]
    return columns





