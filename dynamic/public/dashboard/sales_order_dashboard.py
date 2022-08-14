
from frappe import _
from frappe import get_active_domains
DOMAINS = get_active_domains()


def get_data(data={}):
    dashboard_data = {
        'fieldname': 'sales_order',
        'non_standard_fieldnames': {
            'Journal Entry': 'reference_name',
        },
        "transactions": []
    }
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
