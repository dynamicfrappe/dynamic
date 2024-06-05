# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_date(filters)
    summary = get_report_summary(data)
    return columns, data, None, None, summary

def get_report_summary(data):
    if not data:
        return None

    total_quotation_rate = round(sum([float(row.get("qoutation_rate") or 0) for  row in data]),2)
    total_of_total_cost = round(sum([float(row.get("total_cost") or 0) for  row in data]),2)
    total_difference  = round(sum([float(row.get("total_difference") or 0) for  row in data]),2)
    ratio = calc_ratio(total_of_total_cost, total_difference)
    return[
        {
            'value' : total_quotation_rate,
            'indicator' : 'Blue',
            'label' : _('Total Quotation Rate'),
            'datatype' : 'Currency',
        },
        {
            'value' : total_of_total_cost,
            'indicator' : 'Blue',
            'label' :  _('Total Of Average Cost'),
            'datatype' : 'Currency',
        },
        {
            'value' : total_difference,
			'indicator' : 'Green' if ratio >0 else 'Red',
            'label' : _('Total Difference'),
            'datatype' : 'Currency',
        },
        {
            'value' : ratio,
            'indicator' : 'Green' if ratio >0 else 'Red',
            'label' : _('Ratio'),
            'datatype' : 'Percent',
        }
    ]

def calc_ratio(total_of_total_cost, total_difference):
    ratio = 0.0
    if total_of_total_cost:
        ratio  = (total_difference/total_of_total_cost) *100
    else:
        frappe.msgprint("Total Of Average Cost is Zero. Can't calculate the ratio.")
    return ratio

def get_date(filters):
    conditions = " 1=1 "
    if filters.get("party_name"):
        conditions += f""" and so.party_name = "{filters.get('party_name')}" """
    if filters.get("quotation"):
        conditions += f""" and so.name = "{filters.get('quotation')}" """
    if filters.get("date"):
        conditions += f""" and so.transaction_date = date("{filters.get('date')}") """
    if filters.get("price_list"):
        conditions += f""" and so.selling_price_list = "{filters.get('price_list')}" """
    if filters.get("sales_person"):
        conditions += f""" and st.sales_person = "{filters.get('sales_person')}" """
    if filters.get("warehouse"):
        conditions += f""" and soi.warehouse = "{filters.get('warehouse')}" """     

    sql_query = f"""
        SELECT 
            so.name AS quotation_name,
            soi.item_code,
            soi.item_name,
            soi.qty,
            soi.rate AS qoutation_rate,
            (SELECT pii.rate 
             FROM `tabPurchase Invoice` pi
             INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
             WHERE pi.docstatus = 1
             ORDER BY pi.creation DESC
             LIMIT 1) AS purchase_rate,
            soi.qty * (SELECT pii.rate 
                       FROM `tabPurchase Invoice` pi
                       INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                       WHERE pi.docstatus = 1
                       ORDER BY pi.creation DESC
                       LIMIT 1) AS total_cost,
            soi.rate - (SELECT pii.rate 
                         FROM `tabPurchase Invoice` pi
                         INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                         WHERE pi.docstatus = 1
                         ORDER BY pi.creation DESC
                         LIMIT 1) AS difference,
            soi.qty * (soi.rate - (SELECT pii.rate 
                                   FROM `tabPurchase Invoice` pi
                                   INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                                   WHERE pi.docstatus = 1
                                   ORDER BY pi.creation DESC
                                   LIMIT 1)) AS total_difference,
            ((soi.rate - (SELECT pii.rate 
                           FROM `tabPurchase Invoice` pi
                           INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                           WHERE pi.docstatus = 1
                           ORDER BY pi.creation DESC
                           LIMIT 1)) / (SELECT pii.rate 
                                        FROM `tabPurchase Invoice` pi
                                        INNER JOIN `tabPurchase Invoice Item` pii ON pi.name = pii.parent
                                        WHERE pi.docstatus = 1
                                        ORDER BY pi.creation DESC
                                        LIMIT 1)) * 100 AS difference_percentage
        FROM 
            `tabQuotation` so
        INNER JOIN 
            `tabQuotation Item` soi ON so.name = soi.parent
        LEFT JOIN
            `tabSales Team` st ON so.name = st.parent
        WHERE {conditions}
        """
        
    result = frappe.db.sql(sql_query, as_dict=True)
    return result






def get_columns():
    return[
        {
            "fieldname": "quotation_name",
            "label": _("Quotation"),
            "fieldtype": "Link",
            "options": "Quotation",
            "width": 200,
        },
        {
            "fieldname": "item_code",
            "label": _("Item code"),
            "fieldtype": "Data",
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
            "fieldname": "qoutation_rate",
            "label": "Quotation Rate",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 100,
        },
        {
            "fieldname": "purchase_rate",
            "label": "Rate for Price List",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 100,
        },
        {
            "fieldname": "total_cost",
            "label": "Total Cost",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 100,
        },
        {
            "fieldname": "difference",
            "label": "Difference",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 100,
        },
        {
            "fieldname": "total_difference",
            "label": "Total Difference",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 100,
        },
        {
            "fieldname": "difference_percentage",
            "label": _("Difference Percentage"),
            "fieldtype": "Percent",
            "width": 100,
        }
        # {
        # 	"fieldname": "sales_rate",
        # 	"label": "Sales Rate",
        # 	"fieldtype": "Currency",
        # 	"options": "currency",
        # 	"width": 100,
        # },
        # {
        # 	"fieldname": "total_sales",
        # 	"label": "Total Sales",
        # 	"fieldtype": "Currency",
        # 	"options": "currency",
        # 	"width": 100,
        # },
        # {
        # 	"fieldname": "differance",
        # 	"label": "Differance",
        # 	"fieldtype": "Currency",
        # 	"options": "currency",
        # 	"width": 100,
        # },
        # {
        # 	"fieldname": "total_difference",
        # 	"label": "Total Difference",
        # 	"fieldtype": "Currency",
        # 	"options": "currency",
        # 	"width": 100,
        # },
        # {
        # 	"fieldname": "differance_percentage",
        # 	"label": _("Differance Percentage"),
        # 	"fieldtype": "Data",
        # 	"width": 100,
        # }
    ]



