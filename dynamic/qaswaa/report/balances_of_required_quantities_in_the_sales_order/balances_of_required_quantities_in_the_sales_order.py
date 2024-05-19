

import frappe
from frappe import _
from erpnext.stock.utils import get_stock_balance

def execute(filters=None):
	columns, data = get_columns(), get_date(filters)
	return columns, data



def get_columns():
    return[
        {
            "fieldname": "name",
            "label": _("ID"),
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 200,
        },
        {
            "fieldname": "item_code",
            "label": _("Item code"),
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
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
            "fieldtype": "Data",
            "width": 50,
        },
        {
            "fieldname": "warehouse",
            "label": _("Warehouse"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "stock_balance",
            "label": _("Stock Balance"),
            "fieldtype": "Data",
            "width": 100,
        }
    ]

def get_date(filters):
    conditions = "1=1"
    sql_join = ""
    data = []

    if filters.get("sales_order"):
        conditions += f" and Q.name = '{filters.get('sales_order')}' "
    if filters.get("customer"):
        conditions += f" and Q.customer = '{filters.get('customer')}' "
    
    if filters.get("cost_center"):
        sql_join += """
            INNER JOIN `tabSales Order Item` sii_cc ON si_cc.name = sii_cc.parent
        """
        conditions += f" AND sii_cc.cost_center = '{filters.get('cost_center')}'"   
    
    warehouses = frappe.get_all("Warehouse", filters={"disabled": 0}, pluck="name")

    for warehouse in warehouses:
        sql_join = ""

        if filters.get("warehouse"):
            sql_join += f"""
                INNER JOIN `tabSales Order Item` QI_cc ON Q.name = QI_cc.parent
                AND QI_cc.warehouse = '{warehouse}'
            """

        sql = f'''
            SELECT
                Q.name, QI.item_code, QI.item_name, QI.qty
            FROM 
                `tabSales Order` Q
            INNER JOIN 
                `tabSales Order Item` QI
            ON 
                Q.name = QI.parent
            {sql_join}
            WHERE {conditions}    
        '''

        warehouse_data = frappe.db.sql(sql, as_dict=1)

        for item in warehouse_data:
            stock_balance = get_stock_balance(item['item_code'], warehouse)
            if stock_balance > 0:
                item['stock_balance'] = stock_balance
                item['warehouse'] = warehouse
                data.append(item)

    return data




