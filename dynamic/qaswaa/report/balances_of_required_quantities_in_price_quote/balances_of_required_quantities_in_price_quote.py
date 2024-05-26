# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

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
            "options": "Quotation",
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
    data = []
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if from_date:
        conditions += f" and Q.transaction_date >= '{from_date}'"
    if to_date:
        conditions += f" and Q.transaction_date <= '{to_date}'" 
    if filters.get("quotation"):
        conditions += f" and Q.name = '{filters.get('quotation')}' "
    if filters.get("party_name"):
        conditions += f" and Q.party_name = '{filters.get('party_name')}' "
    if filters.get("cost_center"):
        conditions += f" and Q.cost_center = '{filters.get('cost_center')}' "
    if filters.get("sales_person"):
        conditions += f" and st.sales_person = '{filters.get('sales_person')}' "
    if filters.get("warehouse"):
        conditions += f" and QI.warehouse = '{filters.get('warehouse')}' "           
    
    warehouses = frappe.get_all("Warehouse", filters={"disabled": 0}, pluck="name")

    for warehouse in warehouses:
        sql = f'''
                SELECT
                    Q.name, QI.item_code, QI.item_name, QI.qty
                FROM 
                    `tabQuotation` Q
                INNER JOIN 
                    `tabQuotation Item` QI
                ON 
                    Q.name = QI.parent
                LEFT JOIN
                    `tabSales Team` st ON Q.name = st.parent   

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


