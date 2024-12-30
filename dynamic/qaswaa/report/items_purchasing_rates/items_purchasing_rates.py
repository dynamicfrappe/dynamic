import frappe

def get_data(filters=None):
    conditions = " 1=1 "

    if filters.get("item"):
        conditions += f""" AND pi.item_code = '{filters.get("item")}'"""
    
    if filters.get("item_name"):
        conditions += f""" AND i.item_name = '{filters.get("item_name")}'"""
    
    if filters.get("supplier_name"):
        conditions += f""" AND s.supplier_name = '{filters.get("supplier_name")}'"""
    
    if filters.get("supplier"):
        conditions += f""" AND p.supplier = '{filters.get("supplier")}'"""
    
    if filters.get("date_from"):
        conditions += f""" AND p.posting_date >= '{filters.get("date_from")}'"""
    
    if filters.get("date_to"):
        conditions += f""" AND p.posting_date <= '{filters.get("date_to")}'"""

    query = f"""
        WITH ranked_items AS (
            SELECT 
                pi.item_code,
                i.item_name,
                pi.rate AS purchase_rate,
                p.posting_date,
                ROW_NUMBER() OVER (
                    PARTITION BY pi.item_code 
                    ORDER BY p.posting_date DESC
                ) AS row_num
            FROM 
                `tabPurchase Invoice Item` pi
            JOIN 
                `tabItem` i ON pi.item_code = i.item_code
            JOIN 
                `tabPurchase Invoice` p ON pi.parent = p.name
            WHERE 
                pi.docstatus = 1
                AND p.status != 'Return'""
                AND {conditions}
        ),
        last_three_rates AS (
            SELECT 
                item_code,
                item_name,
                MAX(CASE WHEN row_num = 1 THEN purchase_rate END) AS rate_1,
                MAX(CASE WHEN row_num = 2 THEN purchase_rate END) AS rate_2,
                MAX(CASE WHEN row_num = 3 THEN purchase_rate END) AS rate_3
            FROM ranked_items
            WHERE row_num <= 3
            GROUP BY item_code, item_name
        )
        SELECT 
            item_code,
            item_name,
            rate_1,
            rate_2,
            rate_3
        FROM 
            last_three_rates
        ORDER BY 
            item_code
    """
    # Execute the query with filters
    data = frappe.db.sql(query, filters, as_dict=True)
    return data

def get_columns():
    return [
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Last Purchase Rate",
            "fieldname": "rate_1",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Second Last Purchase Rate",
            "fieldname": "rate_2",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Third Last Purchase Rate",
            "fieldname": "rate_3",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
