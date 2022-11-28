import frappe

from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry as ERPNextPaymentEntry
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder as ERPNextSalesOrder
from erpnext.selling.doctype.quotation.quotation import Quotation as ERPNextQuotation


# Default ERP Class
PaymentEntry = ERPNextPaymentEntry
SalesOrder = ERPNextSalesOrder
Quotation = ERPNextQuotation


active_domains = frappe.get_active_domains()




if "Terra" in active_domains:
    from dynamic.terra.doctype.payment_entry.payment_entry import PaymentEntry as TerraPaymentEntry
    from dynamic.terra.doctype.sales_order.sales_order import SalesOrder as TerraSalesOrder
    from dynamic.terra.doctype.quotation.quotation import Quotation as TerraQuotation

    PaymentEntry = TerraPaymentEntry

    SalesOrder = TerraSalesOrder

    Quotation = TerraQuotation
