import frappe
from frappe import _



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1"

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
    # if filters.get("cost_center"):
    #     conditions += f" and sii_cc.cost_center = '{filters.get('cost_center')}'"
    #     sql_join += """
    #     INNER JOIN `tabSales Invoice Item` sii_cc ON SI.name = sii_cc.parent
    #         """
    # if filters.get("warehouse"):
    #     conditions += f" and sii_cc.warehouse = '{filters.get('warehouse')}'"
    #     sql_join += """
    #     INNER JOIN `tabSales Invoice Item` sii_cc ON SI.name = sii_cc.parent
    #         """
    # if filters.get("sales_person"):
    #     conditions += f" and sii_cc.sales_person = '{filters.get('sales_person')}'"
    #     sql_join += """
    #     INNER JOIN `tabSales Team` sii_cc ON SI.name = sii_cc.parent
    #         """         

    
    sql = '''
        SELECT
            SI.customer, 
            SII.item_code,
            SII.item_name,
            SUM(CASE WHEN SI.status = 'Overdue' THEN SII.qty ELSE 0 END) AS qty_overdue
        FROM
            `tabSales Invoice` SI
        LEFT JOIN
            `tabSales Invoice Item` SII
        ON 
            SI.name = SII.parent
        WHERE
            SI.docstatus = 1
            AND SI.status = 'Overdue'
            AND SI.name IN (
                SELECT return_against 
                FROM `tabSales Invoice` 
                WHERE status = 'Return' AND return_against IS NOT NULL
            )
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
            "fieldname": "qty_overdue", 
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

