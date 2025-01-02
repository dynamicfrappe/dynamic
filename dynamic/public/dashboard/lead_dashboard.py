
from frappe import _
from frappe import get_active_domains
DOMAINS = get_active_domains()


def get_data(data={}):
    if "Logistics" in DOMAINS:
       
        data['transactions'].append(
            {
                'label': _('Actions'),
                'items': ['Actions']
            }
        )
        data['non_standard_fieldnames']['Actions']="document_name"

    return data

    
