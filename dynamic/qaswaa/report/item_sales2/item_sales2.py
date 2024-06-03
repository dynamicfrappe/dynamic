import frappe
from frappe import _



def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_data(filters):
    conditions = " 1=1 "
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    item_code = filters.get("item_code")
    item_group = filters.get("item_group")
    customer = filters.get("customer")
    cost_center = filters.get("cost_center")
    warehouse = filters.get("warehouse")
    sales_person = filters.get("sales_person")

    if from_date:

        conditions += f""" AND s.posting_date >= date('{from_date}')"""
    if to_date:

        conditions += f""" AND s.posting_date >= '{from_date}'"""
    if customer:
        conditions += f""" AND s.customer = '{customer}'"""
    if cost_center:
        conditions += f""" AND s.cost_center = '{cost_center}'"""        
    if item_code:
        conditions += f""" AND si.item_code = '{item_code}'"""
    if warehouse:
        conditions += f""" AND si.warehouse = '{warehouse}'"""    
    if item_group:
        conditions += f""" AND i.item_group = '{item_group}'"""
    if sales_person:
        conditions += f""" AND st.sales_person = '{sales_person}'"""
    data = frappe.db.sql(f"""
        SELECT 
            si.item_code,
            si.item_name,
            si.qty AS qty_difference1,
            si.net_amount AS net_amount_difference1,
            (SELECT qty 
            FROM `tabSales Invoice Item` 
            WHERE parent = s2.name 
            AND item_code = si.item_code 
            LIMIT 1) AS qty_difference2,
            (SELECT net_amount 
            FROM `tabSales Invoice Item` 
            WHERE parent = s2.name 
            AND item_code = si.item_code 
            LIMIT 1) AS net_amount_difference2,
            si.qty + IFNULL((SELECT qty 
                    FROM `tabSales Invoice Item` 
                    WHERE parent = s2.name 
                     AND item_code = si.item_code 
                 LIMIT 1), 0) AS qty_difference,
            si.net_amount + IFNULL((SELECT net_amount 
                    FROM `tabSales Invoice Item` 
                    WHERE parent = s2.name 
                     AND item_code = si.item_code 
                 LIMIT 1), 0) AS net_amount_difference             
        FROM 
        `tabSales Invoice Item` AS si
        JOIN 
        `tabSales Invoice` AS s
        ON 
            si.parent = s.name
        JOIN
            `tabSales Invoice` AS s2
        ON
            s.name = s2.return_against
        LEFT JOIN
            `tabItem` AS i               
        ON
            si.item_code = i.name
        LEFT JOIN
            `tabSales Team` AS stt
        ON
            stt.parent = s.name
        WHERE
            s.name IN (SELECT DISTINCT return_against FROM `tabSales Invoice` WHERE return_against IS NOT NULL)
            AND {conditions}
    """,  as_dict=True)

    return data




def get_columns():
    return [
        # {
        #    "label": _("ID"), 
        #     "fieldname": "sales_invoice_name", 
        #     "fieldtype": "Link", 
        #     "options": "Sales Invoice", 
        #     "width": 300,  
        # },
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
            "fieldname": "qty_difference", 
            "fieldtype": "Float",
            "width": 200, 
        },
        {
            "label": _("Difference Amount"), 
            "fieldname": "net_amount_difference", 
            "fieldtype": "Currency",
            "options":"currency",
            "width": 200, 
        },
    ]

