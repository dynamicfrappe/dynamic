import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_data(filters):
    conditions = "1=1"
    if filters.get("name"):
        conditions += f" AND di.name = '{filters.get('name')}'"
    if filters.get("customer"):
        conditions += f" AND di.customer = '{filters.get('customer')}'"    
    if filters.get("from_date"):
        conditions += f" AND di.posting_date >= '{filters.get('from_date')}'"
    if filters.get("to_date"):
        conditions += f" AND di.posting_date <= '{filters.get('to_date')}'"
    if filters.get("item_group"):
        conditions += f" AND dii.item_group = '{filters.get('item_group')}'"
    if filters.get("item_code"):
        conditions += f" AND dii.item_code = '{filters.get('item_code')}'"

    sql = f'''
        SELECT
            di.name,
            di.customer,
            di.posting_date, 
            dii.item_code,
            dii.item_name,
            dii.item_group,
            dii.qty,
            dii.price_list_rate,
            dii.incoming_rate,
            (dii.incoming_rate - dii.price_list_rate) as profit,
            (dii.qty * dii.incoming_rate) as total_cost,
            (dii.qty * dii.price_list_rate) as total_rate
        FROM
            `tabDelivery Note` di
        LEFT JOIN
            `tabDelivery Note Item` dii
        ON 
            di.name = dii.parent
        WHERE
            {conditions}
    '''

    data = frappe.db.sql(sql, as_dict=True)
    for row in data:
        row['total_profit'] = row['total_cost'] - row['total_rate']

    return data


def get_columns():
    return [
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 200,
        },
        {
            "fieldname": "name",
            "label": _("Delivery ID"),
            "fieldtype": "Link",
            "options": "Delivery Note",
            "width": 200,
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
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
            "label": _("Item Group"), 
            "fieldname": "item_group", 
            "fieldtype": "Link",
            "options": "Item Group", 
            "width": 200, 
        },
        { 
            "label": _("Quantity"), 
            "fieldname": "qty", 
            "fieldtype": "Float", 
            "width": 200, 
        },
        { 
            "label": _("Rate"), 
            "fieldname": "price_list_rate", 
            "fieldtype": "Currency",
            "options": "currency", 
            "width": 200, 
        },
        { 
            "label": _("Total Rate"), 
            "fieldname": "total_rate",
            "fieldtype": "Currency", 
            "width": 200, 
        },
        { 
            "label": _("Cost"), 
            "fieldname": "incoming_rate", 
            "fieldtype": "Currency", 
            "width": 200, 
        },
        { 
            "label": _("Total Cost"), 
            "fieldname": "total_cost", 
            "fieldtype": "Currency", 
            "width": 200, 
        },
        { 
            "label": _("Profit"), 
            "fieldname": "profit", 
            "fieldtype": "Currency", 
            "width": 200, 
        },
        { 
            "label": _("Total Profit"), 
            "fieldname": "total_profit", 
            "fieldtype": "Currency", 
            "width": 200, 
        },       
    ]