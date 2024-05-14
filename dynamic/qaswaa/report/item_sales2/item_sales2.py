import frappe
from frappe import _



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1"
    sql_join = ""

    if filters.get("from_date"):
        conditions += f" and SI.posting_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" and SI.posting_date <= '{filters.get('to_date')}'"
    if filters.get("customer"):
        conditions += f" and SI.customer = '{filters.get('customer')}'"
    if filters.get("item_code"):
        conditions += f" and SII.item_code = '{filters.get('item_code')}'"
    if filters.get("item_group"):
        conditions += f" and SII.item_group = '{filters.get('item_group')}'"
    if filters.get("cost_center"):
        conditions += f" and sii_cc.cost_center = '{filters.get('cost_center')}'"
        sql_join += """
        INNER JOIN `tabSales Invoice Item` sii_cc ON SI.name = sii_cc.parent
            """
    if filters.get("warehouse"):
        conditions += f" and sii_cc.warehouse = '{filters.get('warehouse')}'"
        sql_join += """
        INNER JOIN `tabSales Invoice Item` sii_cc ON SI.name = sii_cc.parent
            """
    if filters.get("sales_person"):
        conditions += f" and sii_cc.sales_person = '{filters.get('sales_person')}'"
        sql_join += """
        INNER JOIN `tabSales Team` sii_cc ON SI.name = sii_cc.parent
            """         

    
    sql = f'''
        SELECT
            SI.customer, 
            SII.item_code,
            SII.item_name,
            SUM(SII.qty) AS qty,
            SUM(SII.net_amount) AS net_amount,
            SUM(CASE WHEN SI.status = 'overdue' THEN SII.qty ELSE 0 END) AS overdue_qty,
            SUM(CASE WHEN SI.status = 'return' THEN SII.qty ELSE 0 END) AS return_qty,
            SUM(CASE WHEN SI.status = 'overdue' THEN SII.qty ELSE 0 END) - SUM(CASE WHEN SI.status = 'return' THEN SII.qty ELSE 0 END) AS difference_qty,
            SUM(CASE WHEN SI.status = 'overdue' THEN SII.net_amount ELSE 0 END) AS overdue_amount,
            SUM(CASE WHEN SI.status = 'return' THEN SII.net_amount ELSE 0 END) AS return_amount,
            SUM(CASE WHEN SI.status = 'overdue' THEN SII.net_amount ELSE 0 END) - SUM(CASE WHEN SI.status = 'return' THEN SII.net_amount ELSE 0 END) AS difference_amount
        FROM
            `tabSales Invoice` SI
        LEFT JOIN
            `tabSales Invoice Item` SII
        ON 
            SI.name = SII.parent
        {sql_join}
        WHERE
            SI.status IN ('overdue', 'return')
            AND {conditions}
        GROUP BY
            SI.customer, 
            SII.item_code,
            SII.item_name
    '''
    data = frappe.db.sql(sql, as_dict=True)
    return data


def get_columns():
    return [
        { 
            "label": _("Customer"), 
            "fieldname": "customer", 
            "fieldtype": "Link", 
            "options": "Customer", 
            "width": 300, 
        },
        { 
            "label": _("Item Code"), 
            "fieldname": "item_code", 
            "fieldtype": "Link", 
            "options": "Item", 
            "width": 300, 
        }, 
        { 
            "label": _("Item Name"), 
            "fieldname": "item_name", 
            "fieldtype": "Data", 
            "width": 200, 
        },
        {
            "label": _("Difference Quantity"), 
            "fieldname": "qty", 
            "fieldtype": "Float",
            "width": 200, 
        },
        {
            "label": _("Difference Amount"), 
            "fieldname": "net_amount", 
            "fieldtype": "Currency",
            "options":"currency",
            "width": 200, 
        },
    ]

