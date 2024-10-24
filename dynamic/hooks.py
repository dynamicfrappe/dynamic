# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

# from . import JSON as json
# from . import PATH as Path
# from . import OS as os


# import json
# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent
# print ("BASE_DIR ====> " , BASE_DIR)
# DOCTYPE_JS_FILE_PATH = os.path.join(BASE_DIR , 'override_doctype_js.json')


DOCTYPE_JS_FILE_PATH = "../apps/dynamic/dynamic/override_doctype_js.json"


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
app_include_js = [
    "/assets/js/dynamic.min.js",
    "/assets/js/desk_sidebar.min.js",
]

# include js in doctype views
# doctype_js = {"Payment Entry": "public/js/payment_entry.js"}
#
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {
    "Appointment": "public/js/appointment_calendar.js"
    # "doctype" : "public/js/appointment.js"
}


# calendars = ["Appointment"]

doctype_list_js = {
    "Customer": "public/js/customer_list.js",
    "Quotation": "public/js/quotation_list.js",
    "Subscription": "public/js/subscription_list.js",
    "Actions": "public/js/actions_list.js",
    "Lead": "public/js/lead_list.js",
    "Sales Invoice" : "public/js/sales_invoice_list.js"
}

after_install = [
    "dynamic.install.after_install",
    "dynamic.dynamic.utils.create_customizations",
    "dynamic.stock_reservation.setup.setup",
]
after_migrate = [
    "dynamic.install.after_install",
    "dynamic.dynamic.utils.create_customizations",
    "dynamic.stock_reservation.setup.setup",
    "dynamic.ram.controllers.setup.create_domain",
    "dynamic.true_lease.controllers.setup.create_domain"
]
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config
override_doctype_class = {
    "Product Bundle": "dynamic.product_bundle.doctype.product_bundle.product_bundle.ProductBundle",
    "Payment Entry": "dynamic.override_doctype_class.PaymentEntry",
    "Quotation": "dynamic.override_doctype_class.Quotation",
    "Sales Order": "dynamic.override_doctype_class.SalesOrder",
    "Salary Slip": "dynamic.override_doctype_class.SalarySlip",
    "Sales Invoice": "dynamic.override_doctype_class.SalesInvoice",
    "Customer": "dynamic.teba.doctype.customer.CustomerController",
    "Stock Entry": "dynamic.override_doctype_class.StockEntry",
    "Subscription": "dynamic.override_doctype_class.Subscription"
    # "Lead" : "dynamic.override_doctype_class.Lead"
    # "Delivery Note": "dynamic.gebco.doctype.sales_invocie.deleivery_note.DeliveryNote"
    # "Sales Order": "dynamic.terra.sales_order"
}
# /home/abanoub/frappe-13/apps/frappe/frappe/public/js/frappe/views/reports/report_view.js
doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js",
    "Sales Order": "public/js/sales_order.js",
    "Stock Entry": 
    [
        "public/js/stock_entry.js",
        "qaswaa/controllers/js/stock_entry.js",
    ],
    "Purchase Order": "public/js/purchase_order.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Product Bundle": "product_bundle/doctype/product_bundle/product_bundle.js",
    "Payment Entry": "public/js/payment_entry.js",
    "Landed Cost Voucher": "public/js/landed_cost_voucher.js",
    "Delivery Note": 
    [
        "public/js/delivery_note.js",
        "qaswaa/controllers/js/delivery_note.js"
    ],
    "Lead": "public/js/lead.js",
    "Supplier": "public/js/supplier.js",
    "Customer": "public/js/customer.js",
    "Quotation": "public/js/quotation.js",
    "Opportunity": "public/js/opportunity.js",
    "Material Request": "public/js/material_request.js",
    "Work Order": "public/js/work_order.js",
    "Job Card": "public/js/job_card.js",
    "Request for Quotation": "public/js/request_for_quotation.js",
    "Mode of Payment": "public/js/mode_of_payment.js",
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "Stock Reconciliation": "public/js/stock_reconciliation.js",
    "Item": [
        "public/js/item.js",
        "qaswaa/controllers/js/item.js"],
    "Journal Entry": "public/js/journal_entry.js",
    "Payment Terms Template": "public/js/payment_terms_template.js",
    "Payment Terms Template": "public/js/payment_terms_template.js",
    "Asset": "public/js/asset.js",
    "Actions": "public/js/actions.js",
    "Subscription": "public/js/subscription.js"
    # "Project RS":"public/js/custom_project_rs.js",
    # "Assign To":"public/sidebar/assign_to.js",    Journal Entry
}
# doctype_js = {
#     "Sales Invoice": "public/js/sales_invoice.js",
#     "Sales Order": "public/js/sales_order.js",
#     "Stock Entry": "public/js/stock_entry.js",
#     "Purchase Order": "public/js/purchase_order.js",
#     "Purchase Invoice": "public/js/purchase_invoice.js",
#     "Product Bundle": "product_bundle/doctype/product_bundle/product_bundle.js",
#     "Payment Entry": "public/js/payment_entry.js",
#     "Landed Cost Voucher": "public/js/landed_cost_voucher.js",
#     "Delivery Note": "public/js/delivery_note.js"
# }


#! added in terra only comment it in another domains
# doctype_js ["Payment Entry"] = "terra/doctype/payment_entry/payment_entry.js"


# override_doctype_js = open(DOCTYPE_JS_FILE_PATH)
# doctype_js = json.load(override_doctype_js)

# print("doctype_js ===========> " , doctype_js.get("Payment Entry"))

doc_events = {
    "Batch":{
        "before_insert":"dynamic.controllers.batch.befor_naming",
    },
    "Payment Entry": {
        "on_submit": "dynamic.api.submit_payment",
    },
    "Sales Invoice": {
        # "before_submit": ["dynamic.api.check_crean_amount_after_mapped_doc",],
        "on_submit": [
            "dynamic.gebco.api.validate_sales_invoice",
            "dynamic.controllers.sales_invoice.before_submit",
            
        ],
        "validate": [
            "dynamic.controllers.sales_invoice.validate",
            "dynamic.api.validate_active_domains",
            "dynamic.controllers.sales_invoice.after_submit",
            
        ],
        # "before_save":"dynamic.controllers.sales_invoice.before_save",
        "on_cancel": [
            "dynamic.api.invoice_on_cancel",
            "dynamic.controllers.sales_invoice.after_cancel",
        ],
        "before_insert": "dynamic.api.before_insert_invoice",
        # "before_cancel" : "dynamic.api.before_cancel_invoice",
    },
    "Item": {
        "autoname": "dynamic.api.autoname",
        "validate": [
            "dynamic.dynamic.validation.validate_item_code",
        ],
        # "before_insert": "dynamic.dynamic.validation.before_insert_item",
        "after_insert": "dynamic.dynamic.validation.after_insert_variant_item",
    },
    "Delivery Note": {
        "on_submit": [
            "dynamic.gebco.api.validate_delivery_note",
            "dynamic.controllers.delivery_note.after_submit",
        ],
        # "before_submit": ["dynamic.api.delivery_note_before_submit"],
        "validate": [
            "dynamic.controllers.delivery_note.validate_delivery_note",
            "dynamic.api.validate_delivery_note",
            "dynamic.weh.delevery_note.validate_delevery_note",
            "dynamic.terra.delivery_note.validate_terra_delievery_not"
            # "dynamic.master_deals.master_deals_api.delivery_note_validate_item_qty",
        ],
        "before_save":[


             "dynamic.master_deals.master_deals_api.get_avail_qty_in_draft_delivery",
        ],
        "on_cancel": [
            "dynamic.controllers.delivery_note.after_cancel",
        ],


    },
    "Journal Entry": {
        "before_submit": ["dynamic.controllers.journal_entry.before_submit_journal_entry"],
        "on_submit": "dynamic.api.submit_journal_entry",
    },
    "Sales Order": {
        "before_submit": ["dynamic.api.before_submit_so"],
        "before_save": [
            "dynamic.api.check_source_item",
        ],
        "validate": [
            "dynamic.elevana.hooks.add_partener_to_sales_order",
            "dynamic.controllers.sales_order.validate_sales_order",
            "dynamic.controllers.sales_order.validate_sales_order_for_stock",
                    ],
        "on_cancel": [
            "dynamic.api.cancel_reservation",
            "dynamic.controllers.sales_order.on_cancel",
            ],
        "on_submit": [
            "dynamic.real_state.rs_api.so_on_submit",
            "dynamic.controllers.sales_order.on_submit",
        ],
        "before_update_after_submit":[
            "dynamic.controllers.sales_order.on_update"
        ],
    },
    "Coupon Code": {
        # this hook will apply only elevana Domain to send coupon code to woo commerce api
        "after_insert": [
            "dynamic.elevana.api.create_new_code",
        ],
        "validate": [
            "dynamic.elevana.api.create_new_code",
        ],
    },
    "Material Request": {
        "on_submit": ["dynamic.api.validate_material_request",
                     ],
        "validate": "dynamic.api.onsave_material_request",
        "before_save":[
            "dynamic.controllers.stock_entry.update_target_warehouse"
        ],
        "on_cancel" :"dynamic.controllers.material_request.on_cancel"
    },
    "Landed Cost Voucher": {
        "validate": "dynamic.dynamic.validation.validate_landed_cost"
    },
    "Purchase Invoice": {
        "validate":"dynamic.yt_minds.controllers.purchase_invoice.validate",
        "on_submit": "dynamic.api.submit_purchase_invoice",
        "before_submit": [
            "dynamic.api.check_crean_amount_after_mapped_doc",
        ],
    },
    "Stock Entry": {
        # In This Target check the branches data in cost center


        "validate": [
            "dynamic.api.validate_stock_entry",  
            "dynamic.master_deals.master_deals_api.get_avail_qty_in_draft_stock_entry",
            "dynamic.controllers.stock_entry.validate",


        ],
        "before_save":[
            #  "dynamic.master_deals.master_deals_api.get_avail_qty_in_draft_stock_entry",
             "dynamic.controllers.stock_entry.before_save_stock_entry"
        ],
        "on_submit": "dynamic.api.submit_stock_entry",
    },
    "Opportunity": {
        "validate": "dynamic.ifi.api.opportunity_notifiy",
        #    "on_submit" : "dynamic.ifi.api.opportunity_notifiy"
    },
    "Payment Entry": {
        "autoname": "dynamic.api.modeofpaymentautoname",
        "validate": "dynamic.api.validate_paymentrntry",
        "on_update_after_submit": "dynamic.api.update_paymentrntry",
    },
    "Asset Movement": {"on_submit": "dynamic.api.add_cost_center_to_asset"},
    "Supplier Quotation": {
        #  "validate" : "dynamic.terra.api.submit_supplier_quotation",
        "on_submit": "dynamic.terra.api.submit_supplier_quotation"
    },
    "Item Price": {"before_save": "dynamic.ifi.api.check_buying_price"},
    "Quotation": {
        # "after_insert":"dynamic.ifi.api.quotation_send_email_cc",
        "validate":"dynamic.qaswaa.controllers.quotation.validate",
        "before_submit": "dynamic.api.before_submit_quot",
        "before_save": "dynamic.api.before_save_quotation",
        "on_cancel" :"dynamic.api.on_cencel" ,
        "validate":"dynamic.yt_minds.controllers.quotation.validate",
    },
    "Purchase Order": {
        # "validate":"dynamic.ifi.api.send_mail_supplier_ifi_po",
        "validate":"dynamic.qaswaa.controllers.purchase_order.validate",
        "before_submit": "dynamic.api.before_submit_po",
        "after_inser": "dynamic.api.calculate_orderd_qty",
        "on_submit": "dynamic.api.calculate_orderd_qty",
        "validate":"dynamic.yt_minds.controllers.purchase_order.validate",
    },
    # "Appointment" :{
    #     "validate":"dynamic.api.appointment_validate"
    # },
    "Accounts Settings": {"validate": "dynamic.api.onsave_account_settings"},
    "Lead": {
        # "validate":"dynamic.ifi.api.lead_contact_by_email"/
        "before_insert": "dynamic.api.lead_before_insert",
        "validate": "dynamic.api.validate_lead" ,
        "on_update": "dynamic.api.on_update" ,

    },
    "Purchase Receipt": {
        "on_submit": [
            "dynamic.api.submit_purchase_recipt",
            "dynamic.api.submit_purchase_recipt_based_on_active_domains",
        ],
        "before_save": "dynamic.api.before_save",
        "validate": [
            "dynamic.controllers.purchase_receipt.validate_purchase_receipt",
        ],
        # "on_submit": "dynamic.gebco.api.validate_purchase_recipt"
        # "before_submit":
        # "before_save":"dynamic.api.check_pr_reservation"
    },
    "Stock Ledger Entry": {
        "before_insert": "dynamic.reservation.reservation_api.stock_ledger_entry_before_insert"
    },
    "File": {
        "after_insert": "dynamic.master_deals.master_deals_api.deals_after_insert"
    },
    "Project":{
        "validate": [
            "dynamic.skyline.controllers.skyline_api.set_total_amounts",
        ],
    }
    # "Batch":{
    #     "before_save": "dynamic.api.disable_batch_if_qty_zero"
    # }
    # "Purchase Receipt": {
    #     "validate": "dynamic.ifi.api.email_supplier_invoice",
    #  },Installations Furniture
    # "Installations Furniture": {
    #     "before_submit": "dynamic.ifi.api.check_child_table_qty",
    #  },
}


# Document Events
# ---------------
# Hook on document methods and events


# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "*/1 * * * *": ["dynamic.logistics.logistics_api.check_data_remaining"],
        "0 */2 * * *": [
            "dynamic.gebco.doctype.maintenance_contract.maintenance_contract.update_contract_status",
            "erpnext.stock.reorder_item.reorder_item",
        ],
        "0 11 * * *": [
            "dynamic.api.saftey_stock",
        ],
        "0 */12 * * *": [
            "dynamic.api.validate_sales_order_reservation_status",
        ],
        "0 13 * * *": [
            "dynamic.product_bundle.doctype.packed_item.new_packed_item.get_old_invocie"
        ],
        "* 8 * * *": [
            # "dynamic.ifi.api.send_mail_daily_opportunity_lead",
            # "dynamic.ifi.api.daily_opportunity_notify"
        ],
    },
    # 	"all": [
    # 		"dynamic.tasks.all" from dynamic.controllers.opportunity import close_ended_opportunity
    # 	],
    "daily": [
        "dynamic.dynamic.doctype.sales_person_commetion.sales_person_commetion.update_month_previous_logs",
        "dynamic.master_deals.master_deals_api.alert_cheque_date",
        "dynamic.real_state.rs_api.setup_payment_term_notify",
        #"dynamic.controllers.opportunity.close_ended_opportunity"
        # "dynamic.alrehab.doctype.installment_entry.installment_entry.get_installment_entry_to_update_status",
    ],
    "hourly": [
        # "dynamic.tasks.hourly",
        "dynamic.dynamic.api.cor_job_cancel_reservation"
    ],
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
override_whitelisted_methods = {
    # "frappe.desk.reportview.export_query": "dynamic.api.export_query",
    # "frappe.desk.doctype.event.event.get_events": "dynamic.event.get_events"
    # /home/abanoub/frappe/dynamc_projects/frappe-14/apps/erpnext/erpnext/controllers/queries.py
    # "erpnext.controllers.queries.supplier_query":"dynamic.master_deals.master_deals_api.get_supplier_by_code"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps


override_doctype_dashboards = {
    "Sales Invoice": "dynamic.public.dashboard.sales_invoice_dashboard.get_data",
    "Sales Order": "dynamic.public.dashboard.sales_order_dashboard.get_data",
    "Purchase Invoice": "dynamic.public.dashboard.purchase_invoice_dashboard.get_data",
    "Purchase Order": "dynamic.public.dashboard.purchase_order_dashboard.get_data",
    "Payment Entry": "dynamic.public.dashboard.payment_entry_dashboard.get_data",
    "Work Order": "dynamic.public.dashboard.work_order.get_data",
    "Job Card": "dynamic.public.dashboard.job_card.get_data",
    "Opportunity": "dynamic.public.dashboard.opportunity_dashboard.get_data",
    "Customer": "dynamic.public.dashboard.customer_dashboard.get_data",
    "Subscription": "dynamic.public.dashboard.subscription_dashboard.get_data",

}

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


domains = {
    "Dynamic Accounts": "dynamic.domains.dynamic_accounts",
    "Dynamic HR": "dynamic.domains.dynamic_hr",
    "Dynamic Payroll": "dynamic.domains.dynamic_payroll",
    "Gebco": "dynamic.domains.gebco",
    "Moyate": "dynamic.domains.moyate",
    "Product Bundle": "dynamic.domains.product_bundle",
    "Cheques": "dynamic.domains.cheques",
    "Terra": "dynamic.domains.tera",
    "IFI": "dynamic.domains.ifi",
    "textile": "dynamic.domains.textile",
    "vero": "dynamic.domains.vero",
    "Reach Group": "dynamic.domains.reach_group",
    "Vana": "dynamic.domains.vana",
    "Merge Entries": "dynamic.domains.merge_entries",
    "WEH": "dynamic.domains.weh",
    "Owais": "dynamic.domains.owais",
    "Elevana": "dynamic.domains.elevana",
    "Homrany": "dynamic.domains.homrany",
    "Teba": "dynamic.domains.teba",
    "Sedia": "dynamic.domains.sedia",
    "Majestey": "dynamic.domains.majestey",
    "Kmina": "dynamic.domains.kmina",
    "Maser2000": "dynamic.domains.maser2000",
    "Behira Pac": "dynamic.domains.behira_pac",
    "Future": "dynamic.domains.future",
    "Elhamd": "dynamic.domains.elhamd",
    "CRM Advance": "dynamic.domains.crm_advance",
    "Reservation": "dynamic.domains.reservation",
    "Real State": "dynamic.domains.real_state",
    "Master Deals": "dynamic.domains.master_deals",
    "Barcode Item": "dynamic.domains.barcode_item",
    "Repack": "dynamic.domains.repack",
    "Clinic": "dynamic.domains.clinic",
    "EGY Phar": "dynamic.domains.egy_phar",
    "ARAM": "dynamic.domains.aram",
    "Branch": "dynamic.domains.branch",
    "Cost Center": "dynamic.domains.cost_center",
    "Lormed": "dynamic.domains.lormed",
    "Nilex": "dynamic.domains.nilex",
    "Stock Transfer": "dynamic.domains.stock_transfer",
    "Qaswaa": "dynamic.domains.qaswaa",
    "Rehab": "dynamic.domains.alrehab",
    "Logistics": "dynamic.domains.logistics",
    "Notebook": "dynamic.domains.notebook",
    "Smart Vision": "dynamic.domains.smart_vision",
    "Stock Reservation": "dynamic.domains.stock_reservation",
    "Ram": "dynamic.domains.ram" , 
    "Pre Quotation": "dynamic.domains.pre_quotation",
    "Skyline": "dynamic.domains.skyline",
    "Healthy Corner":"dynamic.domains.healthy_corner",
    "Payment Deduction": "dynamic.domains.payment_deduction",
    "True lease": "dynamic.domains.truelease",
    "Calculation Sheet":"dynamic.domains.calculation_sheet",
    "YT Minds":"dynamic.domains.yt_minds",
    "Top Laser":"dynamic.domains.toplaser",
    "Trecom":"dynamic.domains.trecom",
}

# domain Conatin
# Moyate
# Add Commition table to sales person and sales invocie
#


jenv = {
    "methods": [
        "get_taxes_amount:dynamic.api.get_taxes_amount",
        "get_components_summary:dynamic.utils.get_components_summary",
        "get_invoice_tax_data:dynamic.utils.get_invoice_tax_data",
        "encode_item_data:dynamic.www.item_data.encode_item_data",
        "get_total_discount_and_amount:dynamic.api.get_total_discount_and_amount",
        "get_total_num_and_qty:dynamic.api.get_total_num_and_qty",
        # "test_encode_item_data:dynamic.www.item_data.test_encode_item_data",
        "encode_invoice_data:dynamic.api.encode_invoice_data",
        "get_company_address:frappe.contacts.doctype.address.address.get_company_address",
        "get_address_display:frappe.contacts.doctype.address.address.get_address_display",
        "get_balance_on:erpnext.accounts.utils.get_balance_on",
        "get_hijri_date:dynamic.api.get_hijri_date",
        "get_cst_address:dynamic.api.get_street_address_html",
        "get_party_address:dynamic.api.get_party_address",  # ifi
        "get_customer_total_unpaid_amount:dynamic.api.get_customer_total_unpaid_amount",
        "QRcode_Customer_data:dynamic.master_deals.master_deals_api.QRcode_Customer_data",
    ],
    "filters": [],
}


fixtures = [
    {
        "dt": ("Custom Field"),
        "filters": [
            [
                "name",
                "in",
                (
                    "Journal Entry Account-party_name",
                    "Cheque-party_name",
                ),
            ]
        ],
    }
]
