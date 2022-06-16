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

# include js, css files in header of web template
# web_include_js = "/assets/dynamic/js/dynamic.js"
# web_include_css = "/assets/dynamic/css/redtheme_web.css"


# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dynamic/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js"}
# doctype_js = {"Payment Entry": "public/js/payment_entry.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "dynamic.install.before_install"
after_install = "dynamic.install.after_install"
after_migrate = "dynamic.install.after_install"
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config


doctype_js = {
    "Customer": "e_invoice/doctype/customer/customer.js",
    "Sales Invoice": "e_invoice/doctype/sales_invoice/sales_invoice.js",
    "Item": "e_invoice/doctype/item/item.js",
    "Sales Order": "public/js/sales_order.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Product Bundle": "product_bundle/doctype/product_bundle/product_bundle.js",
    "Payment Entry": "public/js/payment_entry.js",
    "Item Tax Template":"e_invoice/doctype/item_tax_template/item_tax_template.js"
}
doc_events = {

    "Sales Invoice": {
        "autoname": "dynamic.e_invoice.doctype.sales_invoice.sales_invoice.autoname",
        "on_submit": "dynamic.gebco.api.validate_sales_invoice",
        "validate": "dynamic.api.validate_active_domains"
    },
    "Delivery Note": {
        "on_submit": "dynamic.gebco.api.validate_delivery_note",
        "validate": "dynamic.product_bundle.doctype.packed_item.packed_item.make_packing_list"

    },
    "Stock Entry": {
        "on_submit": "dynamic.contracting.doctype.stock_entry.stock_entry.on_submit"
    },
    "Journal Entry": {
        "on_submit": "dynamic.api.submit_journal_entry"
    },
    "Sales Order": {
        "validate": "dynamic.contracting.doctype.stock_entry.stock_entry.update_project_cost"
    },
    "Purchase Receipt": {
        "on_submit": "dynamic.gebco.api.validate_purchase_recipt"
    },
    "Purchase Order": {
        "on_submit": "dynamic.contracting.doctype.purchase_order.purchase_order.update_comparison",
        "on_cancel": "dynamic.contracting.doctype.purchase_order.purchase_order.update_comparison", }
}
# notification_config = "dynamic.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Product Bundle": "dynamic.product_bundle.doctype.product_bundle.product_bundle.ProductBundle"
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
        ]
    },
    # 	"all": [
    # 		"dynamic.tasks.all"
    # 	],
    # 	"daily": [
    # 		"dynamic.tasks.daily"
    # 	],
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
# override_doctype_dashboards = {
# 	"Task": "dynamic.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


domains = {
    'Dynamic Accounts': 'dynamic.domains.dynamic_accounts',
    'Dynamic HR': 'dynamic.domains.dynamic_hr',
    'E Invoice': 'dynamic.domains.e_invoice',
    'Contracting': 'dynamic.domains.contracting',
    'Gebco': 'dynamic.domains.gebco',
    "Moyate": 'dynamic.domains.moyate',
    'Product Bundle': 'dynamic.domains.product_bundle',
    'Cheques': 'dynamic.domains.cheques',
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
