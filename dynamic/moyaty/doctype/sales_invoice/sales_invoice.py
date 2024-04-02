
import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from dynamic.api import encode_invoice_data
from dynamic.api import delete_update_commission_sales
#from erpnext.regional.saudi_arabia.utils import create_qr_code
from dynamic.moyaty.doctype.sales_invoice.vat_qr import create_qr_code
class CustomSalesInvoice(SalesInvoice):

    def on_trash(self):
        delete_update_commission_sales(self)





def create_sales_invoice_qr_code(doc) :
    create_qr_code(doc)




