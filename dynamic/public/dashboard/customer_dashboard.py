from frappe import _
from frappe import get_active_domains

DOMAINS = get_active_domains()


def get_data(data={}):
    if "Terra" in DOMAINS:
        data["non_standard_fieldnames"].update(
            {"Actions": "customer", "Appointment": "party"}
        )
        data["transactions"].append(
            {"label": _("Actions"), "items": ["Appointment", "Actions"]}
        )
    if "True lease" in DOMAINS:
        data["non_standard_fieldnames"].update({"Contract": "party_name"})
        print(data)
        data["transactions"].append({"label": _("Contracts"), "items": ["Contract"]})
    return data


def get_dasssta():
    return {
        "fieldname": "name",
        "non_standard_fieldnames": {
            "Delivery Note": "against_sales_invoice",
            "Journal Entry": "reference_name",
            "Payment Entry": "reference_name",
            "Payment Request": "reference_name",
            "Sales Invoice": "return_against",
            "Auto Repeat": "reference_document",
            "Purchase Invoice": "inter_company_invoice_reference",
        },
        "internal_links": {
            "Sales Order": ["items", "sales_order"],
            "Timesheet": ["timesheets", "time_sheet"],
        },
        "internal_and_external_links": {
            "Delivery Note": ["items", "delivery_note"],
        },
        "transactions": [
            {
                "label": _("Payment"),
                "items": [
                    "Payment Entry",
                    "Payment Request",
                    "Journal Entry",
                    "Invoice Discounting",
                    "Dunning",
                ],
            },
            {
                "label": _("Reference"),
                "items": ["Timesheet", "Delivery Note", "Sales Order"],
            },
            {"label": _("Returns"), "items": ["Sales Invoice"]},
            {"label": _("Subscription"), "items": ["Auto Repeat"]},
            {"label": _("Internal Transfers"), "items": ["Purchase Invoice"]},
        ],
    }
