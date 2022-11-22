# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "dynamic"
app_title = "Dynamic"
app_publisher = "Dynamic"
app_description = "Dynamic"
app_icon = "octicon octicon-file-directory"
app_color = "#0e4194"
app_email = "hashirabdulla@gmail.com"
app_license = "MIT"
app_logo_url = "/assets/dynamic/images/dynamic-logo.png"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/dynamic/css/dynamic.css"
app_include_js = "/assets/js/dynamic.min.js"



# include js in doctype views
# doctype_js = {"Payment Entry": "public/js/payment_entry.js"}
# 
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_list_js = {
                    "Customer" : "public/js/customer_list.js"
            
                    }

after_install = "dynamic.install.after_install"
after_migrate = "dynamic.install.after_install"
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config


doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "Sales Order": "public/js/sales_order.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Purchase Order": "public/js/purchase_order.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Product Bundle": "product_bundle/doctype/product_bundle/product_bundle.js",
    "Payment Entry": "public/js/payment_entry.js",
    "Landed Cost Voucher": "public/js/landed_cost_voucher.js",
    "Delivery Note": "public/js/delivery_note.js"
}
doc_events = {
    "Payment Entry":{
               "on_submit": "dynamic.api.submit_payment",
    },

    "Sales Invoice": {
        "on_submit": "dynamic.gebco.api.validate_sales_invoice",
        "validate": "dynamic.api.validate_active_domains"
    },
    "Item": {
        "autoname": "dynamic.api.autoname",
        "validate": "dynamic.dynamic.validation.validate_item_code"
    },
    "Delivery Note": {
        "on_submit": "dynamic.gebco.api.validate_delivery_note",
        "validate": "dynamic.api.validate_delivery_note",
        "on_cancel": "dynamic.api.cancel_delivery_note",
    },
   
    "Journal Entry": {
        "on_submit": "dynamic.api.submit_journal_entry"
    },
    "Sales Order": {
        "on_submit": "dynamic.api.create_reservation_validate",
        "before_save": "dynamic.api.check_source_item",
        "on_cancel":"dynamic.api.cancel_reservation",
        "on_update_after_submit":"dynamic.api.change_row_after_submit"
    },
    "Purchase Receipt": {
        # "on_submit": "dynamic.gebco.api.validate_purchase_recipt"
        "on_submit": "dynamic.api.submit_purchase_recipt_based_on_active_domains",
        # "before_save":"dynamic.api.check_pr_reservation"
    },
    "Material Request": {
        "on_submit": "dynamic.api.validate_material_request"

    },
    "Landed Cost Voucher": {
        "validate": "dynamic.dynamic.validation.validate_landed_cost"
    },
    "Purchase Invoice": {
        "on_submit": "dynamic.api.submit_purchase_invoice",
     } 
}

override_doctype_class = {
    "Product Bundle": "dynamic.product_bundle.doctype.product_bundle.product_bundle.ProductBundle",
    # "Delivery Note": "dynamic.gebco.doctype.sales_invocie.deleivery_note.DeliveryNote"
    # "Sales Order": "dynamic.terra.sales_order"
}

# Document Events
# ---------------
# Hook on document methods and events


# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "0 */2 * * *": [
            "dynamic.gebco.doctype.maintenance_contract.maintenance_contract.update_contract_status",
            "erpnext.stock.reorder_item.reorder_item",
        ],
        "0 11 * * *": [
            "dynamic.api.saftey_stock",
        ],
        "0 */12 * * *": [
            "dynamic.api.validate_sales_order_reservation_status",
        ] ,
        "0 13 * * *" :[
            "dynamic.product_bundle.doctype.packed_item.new_packed_item.get_old_invocie"
        ]
    },
    # 	"all": [
    # 		"dynamic.tasks.all"
    # 	],
    	"daily": [
    		"dynamic.dynamic.doctype.sales_person_commetion.sales_person_commetion.update_month_previous_logs"
    	],
    # 	"hourly": [
    # 		"dynamic.tasks.hourly"
    # 	],
    # 	"weekly": [
    # 		"dynamic.tasks.weekly"
    # 	]
    # 	"monthly": [
    # 		"dynamic.tasks.monthly"
    # 	]
}

# Testing
# -------

# before_tests = "dynamic.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dynamic.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps


override_doctype_dashboards = {
    "Sales Invoice": "dynamic.public.dashboard.sales_invoice_dashboard.get_data",
    "Sales Order": "dynamic.public.dashboard.sales_order_dashboard.get_data",
    "Purchase Invoice": "dynamic.public.dashboard.purchase_invoice_dashboard.get_data",
    "Purchase Order": "dynamic.public.dashboard.purchase_order_dashboard.get_data",
    "Payment Entry": "dynamic.public.dashboard.payment_entry_dashboard.get_data"
}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


domains = {
    'Dynamic Accounts': 'dynamic.domains.dynamic_accounts',
    'Dynamic HR': 'dynamic.domains.dynamic_hr',
    'Gebco': 'dynamic.domains.gebco',
    "Moyate": 'dynamic.domains.moyate',
    'Product Bundle': 'dynamic.domains.product_bundle',
    'Cheques': 'dynamic.domains.cheques',
    'Terra': 'dynamic.domains.tera',
}

# domain Conatin
# Moyate
# Add Commition table to sales person and sales invocie
#


jenv = {
    "methods": [
        "get_invoice_tax_data:dynamic.utils.get_invoice_tax_data",
        "encode_invoice_data:dynamic.api.encode_invoice_data",
        "get_company_address:frappe.contacts.doctype.address.address.get_company_address",
        "get_address_display:frappe.contacts.doctype.address.address.get_address_display",
        "get_balance_on:erpnext.accounts.utils.get_balance_on"
    ],
    "filters": []
}
