from __future__ import unicode_literals
from frappe import _ 

data = {
    'custom_fields': {
        'Quotation': [
            {
                "label": _("Last Comment"),
                "fieldname": "last_com_section",
                "fieldtype": "Section Break",
                "insert_after": "lost_reasons",
            },
             {
                "label": _("Last Comment"),
                "fieldname": "last_comment",
                "fieldtype": "Section Break",
                "insert_after": "last_com_section",
            },
        ],
    }

}



