# Copyright (c) 2013, Dynamic Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def get_columns(filters):
    columns = [
        {
            "label": _("Series"),
            "fieldname": "internalid",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Type"),
            "fieldname": "receiver_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Document Type"),
            "fieldname": "document_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver"),
            "fieldname": "receiver",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "label": _("Receiver Id"),
            "fieldname": "receiverid",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver Name"),
            "fieldname": "receivername",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver Type"),
            "fieldname": "receiver_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Receiver Country"),
            "fieldname": "country_code",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Receiver Region City"),
            "fieldname": "regioncity",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver Governate"),
            "fieldname": "governate",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver Street"),
            "fieldname": "street",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver branchID"),
            "fieldname": "branchid",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Receiver Building Number"),
            "fieldname": "buildingnumber",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Date TimeIssued"),
            "fieldname": "datetime_issued",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Internal Id"),
            "fieldname": "internalid",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Code (Item)"),
            "fieldname": "itemcode",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Description (Item)"),
            "fieldname": "description",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("UOM (Item)"),
            "fieldname": "uom",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Item Type (Item)"),
            "fieldname": "item_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("QTY (Item)"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Rate (Item)"),
            "fieldname": "rate",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Discount (Item)"),
            "fieldname": "discount_amount",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Item Tax (Item)"),
            "fieldname": "taxable_item",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Tax Amount"),
            "fieldname": "tax_amount",
            "fieldtype": "Data",
            "width": 100
        },

    ]
    return columns


# `tabCustomer`

def get_data(filters):
    start_date = filters.get('start_date')
    end_date = filters.get('end_date')
    customer = filters.get('customer')
    main_sql = """ 
		SELECT  `tabCustomer`.customer_name AS receivername ,
		        `tabCustomer`.name as receiver ,
				`tabCustomer`.receiver_type as receiver_type  ,
				`tabCustomer`.country_code as country_code ,
				`tabCustomer`.regioncity as regioncity ,
				'i' as document_type,
				`tabCustomer`.governate  as governate,
				`tabCustomer`.street  as street, 
				`tabSales Invoice`.datetime_issued as datetime_issued ,
				`tabSales Invoice`.name as internalid , 
				`tabSales Invoice`.taxable_item AS taxable_item ,
				`tabCustomer`.buildingnumber as buildingnumber ,
				`tabCustomer`.branchid as branchid ,
				`tabCustomer`.receiver_id AS receiverid,
				 0 as 'tax_amount'   
				 FROM `tabSales Invoice`
				 inner join `tabCustomer`  
				 ON `tabSales Invoice`.customer = `tabCustomer`.name 
				 WHERE `tabSales Invoice`.tax_auth = 1 and `tabSales Invoice`.docstatus = 1
		"""

    if start_date:
        start_ql = " AND `tabSales Invoice`.posting_date >= '%s' " % start_date
        main_sql = main_sql + start_ql
    if end_date:
        end_sql = " AND `tabSales Invoice`.posting_date <= '%s' " % end_date
        main_sql = main_sql + end_sql
    if customer:
        customer_sql = " AND `tabSales Invoice`.customer = '%s' " % customer
        main_sql = main_sql + customer_sql
    main_data = frappe.db.sql(main_sql, as_dict=True)
    data = []
    for i in main_data:
        c = frappe.db.sql(""" 
		SELECT 
			itemcode ,description ,uom ,item_type ,qty ,rate ,discount_amount
		 from `tabSales Invoice Item` WHERE parent = '%s'
		""" % i.internalid, as_dict=True)
        if len(c) > 0:
            first_row = {**i, **c[0]}
            data.append(first_row)
        for count in range(1, (len(c))):
            tax_tem = {"taxable_item": i.get('taxable_item')}
            new_line = {**tax_tem, **c[count]}
            data.append(new_line)
    return data


def execute(filters=None):
    # columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data
