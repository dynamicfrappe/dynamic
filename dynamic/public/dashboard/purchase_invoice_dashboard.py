
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
        
    if "Dynamic Accounts" in DOMAINS:
        data["non_standard_fieldnames"].update({"Purchase Receipt": "purchase_invoice"})
        # data["non_standard_fieldnames"].update({"Purchase Order": "purchase_order"})

        if "internal_links" in data:
            data["internal_and_external_links"] = data["internal_links"].copy()

            if "Purchase Receipt" in data["internal_links"]:
                del data["internal_links"]["Purchase Receipt"]

            if "Purchase Order" in data["internal_links"]:
                del data["internal_links"]["Purchase Order"]
                
    return data
