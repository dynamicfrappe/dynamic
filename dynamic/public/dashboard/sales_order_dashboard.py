
from frappe import _
from frappe import get_active_domains
DOMAINS = get_active_domains()


def get_data(data={}):
    if "Cheques" in DOMAINS:
        return {
            'fieldname': 'payment_entry',
            'non_standard_fieldnames': {
                'Journal Entry': 'reference_name',
            },
            'transactions': [
                {
                    'label': _('Journal Entry'),
                    'items': ['Journal Entry']
                },

            ]
        }
    return data

