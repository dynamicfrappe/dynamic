# Copyright (c) 2024, Dynamic and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.meta import get_field_precision
from frappe.utils import cstr, flt
from frappe.utils.xlsxutils import handle_html

# from erpnext.accounts.report.sales_register.sales_register import get_mode_of_payments
from erpnext.selling.report.item_wise_sales_history.item_wise_sales_history import (
	get_customer_details,
	get_item_details,
)


def execute(filters=None):
	return _execute(filters)

