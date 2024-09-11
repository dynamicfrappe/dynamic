import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    summary = get_report_summary(data)
    return columns, data, None, None, summary

def get_report_summary(data):
    if not data:
        return None

    total_rate = round(sum([float(row.get("selling_price_per_qty") or 0) for  row in data]),2)
    total_purchase = round(sum([float(row.get("total_purchase") or 0) for  row in data]),2)
    total_variance  = round(sum([float(row.get("total_variance") or 0) for  row in data]),2)
    ratio = calc_ratio(total_purchase, total_variance)
    return[
        {
            'value' : total_rate,
            'indicator' : 'Blue',
            'label' : _('Total Rate'),
            'datatype' : 'Currency',
        },
        {
            'value' : total_purchase,
            'indicator' : 'Blue',
            'label' :  _('Total Purchase Value'),
            'datatype' : 'Currency',
        },
        {
            'value' : total_variance,
            'indicator' : 'Green' if total_variance > 0 else 'Red',
            'label' : _('Total Variance'),
            'datatype' : 'Currency',
        },
        {
            'value' : ratio,
            'indicator' : 'Green' if ratio > 0 else 'Red',
            'label' : _('Ratio'),
            'datatype' : 'Percent',
        }
    ]

def calc_ratio(total_purchase, total_variance):
    ratio = 0.0
    if total_purchase:
        ratio  = (total_variance/total_purchase) *100
    else:
        frappe.msgprint("Total Purchase value is Zero. Can't calculate the ratio.")
    return ratio

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
    conditions += " AND sd.status NOT IN ('Draft', 'Cancelled')"    

    sql = f'''
        SELECT 
            sd.name AS sales_order,
            item.item_code,
            item.item_name,
            item.qty,
            item.rate,
            item.rate * item.qty AS selling_price_per_qty,
            sle.incoming_rate AS purchase_invoice_rate,
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
        LEFT JOIN
            `tabStock Ledger Entry` sle ON sle.item_code = item.name 
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
            "fieldtype": "Link",
            "options": "Item",
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
            "fieldname": "selling_price_per_qty",
            "label": _("Selling Price Per Qty"),
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





