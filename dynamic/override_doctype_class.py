import json
import frappe

from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry as ERPNextPaymentEntry
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder as ERPNextSalesOrder
from erpnext.selling.doctype.quotation.quotation import Quotation as ERPNextQuotation


# Default ERP Class
PaymentEntry = ERPNextPaymentEntry
SalesOrder = ERPNextSalesOrder
Quotation = ERPNextQuotation


# doctype js override
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "Sales Order": "public/js/sales_order.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Purchase Order": "public/js/purchase_order.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Product Bundle": "product_bundle/doctype/product_bundle/product_bundle.js",
    "Payment Entry": "public/js/payment_entry.js",
    "Landed Cost Voucher": "public/js/landed_cost_voucher.js",
    "Delivery Note": "public/js/delivery_note.js",
    "Lead":"public/js/lead.js",
    "Supplier":"public/js/supplier.js",
    "Customer":"public/js/customer.js",
}

active_domains = frappe.get_active_domains()


# print("override doctype_js in hooks",'hooks.doctype_js')

if "Terra" in active_domains:
    # frappe.msgprint('terra')
    # override doctype clesses
    from dynamic.terra.doctype.payment_entry.payment_entry import PaymentEntry as TerraPaymentEntry
    from dynamic.terra.doctype.sales_order.sales_order import SalesOrder as TerraSalesOrder
    from dynamic.terra.doctype.quotation.quotation import Quotation as TerraQuotation

    PaymentEntry = TerraPaymentEntry

    SalesOrder = TerraSalesOrder

    Quotation = TerraQuotation


    # override doctype js
    doctype_js ["Payment Entry"] = "terra/doctype/payment_entry/payment_entry.js"






# override doctype_js in hooks

# # try :
# from dynamic import override_doctype_js
# # # from hooks import doctype_js
# from dynamic import hooks

# # frappe.msgprint("override doctype_js in hooks")

# hooks.doctype_js = override_doctype_js.doctype_js
# frappe.msgprint(str(hooks.doctype_js))

# except Exception as e  :
    
#     print("override doctype_js in hooks error",str(e))



from dynamic.hooks import DOCTYPE_JS_FILE_PATH
# frappe.msgprint(f'data-->{str(doctype_js)}')
with open(DOCTYPE_JS_FILE_PATH, "w") as write_file:
    
    json.dump(doctype_js, write_file, indent=4)



print ("doctype js override ==========> " , doctype_js.get("Payment Entry"))

