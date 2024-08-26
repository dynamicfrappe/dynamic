
from frappe import _
from frappe import get_active_domains
DOMAINS = get_active_domains()


def get_data(data={}):
    if "Rehab" in DOMAINS:
        data['non_standard_fieldnames'].update({'Journal Entry': "je_ref"})
        data['transactions'].append(
            {
                'label': _('Payment'),
                'items': ['Journal Entry']
            }
        )
    return data
