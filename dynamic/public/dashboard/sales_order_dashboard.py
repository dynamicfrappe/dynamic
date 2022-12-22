
from frappe import _
from frappe import get_active_domains
#/home/beshoy/Dynamic-13/tera/frappe-tera/apps/erpnext/erpnext/selling/doctype/sales_order/sales_order_dashboard.py
# from erpnext.selling.doctype.sales_order.sales_order_dashboard import get_data as dashboard_data_data
DOMAINS = get_active_domains()


def get_data(data={}):
    dashboard_data =data
    if "Cheques" in DOMAINS:
        dashboard_data["transactions"].append(
            {
                'label': _('Journal Entry'),
                'items': ['Journal Entry']
            },
        )

    if "Gebco" in DOMAINS:
        dashboard_data["transactions"].append(
            {
                'label': _('Installation'),
                'items': ['Installation Request', 'Installation Order', 'Car Installation']
            },
        )

    return dashboard_data
