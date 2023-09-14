
import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

from dynamic.api import delete_update_commission_sales

class CustomSalesInvoice(SalesInvoice):

    def on_trash(self):
        delete_update_commission_sales(self)
