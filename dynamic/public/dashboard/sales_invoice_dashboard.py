
from frappe import _
from frappe import get_active_domains
DOMAINS = get_active_domains()


def get_data(data={}):
    

    if "Cheques" in DOMAINS:
        data['non_standard_fieldnames'].update({'Cheque': "reference_name"})
        data['transactions'].append(
            {
                'label': _('Cheques'),
                'items': ['Cheque']
            }
        )
    if "Rehab" in DOMAINS:
        data['non_standard_fieldnames'].update({'Journal Entry': "reference_name"})
        
    return data
