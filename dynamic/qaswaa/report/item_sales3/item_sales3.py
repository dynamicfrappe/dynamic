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
        conditions += f""" AND s.posting_date <= date('{to_date}')"""
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
        SELECT si.item_code, si.item_name, 
               SUM(CASE WHEN s.status != 'Return' THEN si.qty ELSE 0 END) as qty_difference1,
               SUM(CASE WHEN s.status = 'Return' THEN si.qty ELSE 0 END) as qty_difference2,
               (SUM(CASE WHEN s.status != 'Return' THEN si.qty ELSE 0 END) +
                SUM(CASE WHEN s.status = 'Return' THEN si.qty ELSE 0 END)) as qty_difference,
               SUM(CASE WHEN s.status != 'Return' THEN si.net_amount ELSE 0 END) as net_amount_difference1,
               SUM(CASE WHEN s.status = 'Return' THEN si.net_amount ELSE 0 END) as net_amount_difference2,
               (SUM(CASE WHEN s.status != 'Return' THEN si.net_amount ELSE 0 END) +
                SUM(CASE WHEN s.status = 'Return' THEN si.net_amount ELSE 0 END)) as net_amount_difference                             
        FROM `tabSales Invoice` s
        INNER JOIN `tabSales Invoice Item` si ON s.name = si.parent
        INNER JOIN `tabItem` i ON si.item_code = i.name
        LEFT JOIN `tabSales Team` st ON s.name = st.parent
        WHERE {conditions} AND s.docstatus != 2
        GROUP BY si.item_code
    """, as_dict=True)

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

