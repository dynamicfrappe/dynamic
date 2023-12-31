
from frappe import _

data = {
    "custom_fields":{
        "Sales Invoice":[
            {
                "label": "Brand",
                "fieldname": "brand",
                "fieldtype": "Link",
                "insert_after": "customer" ,
                "options": "Brand",
            },
            {
                "label": _("Ignore Validation"),
                "fieldname": "ignore_validation",
                "fieldtype": "Check",
                "insert_after": "due_date" ,
            },

            
        ],
        "Stock Entry":[
            {
                "label": "Stock Entry Transfer Type",
                "fieldname": "stock_entry_transfer_type",
                "fieldtype": "Link",
                "insert_after": "stock_entry_type" ,
                "options": "Stock Entry",
                "depends_on": "eval:doc.stock_entry_type == 'Repack'"
            }
        ]
    }
}