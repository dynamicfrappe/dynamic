from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    "custom_fields": {
        "Item": [
            {
                "label": _("Barcode Second"),
                "fieldname": "barcode",
                "fieldtype": "Data",
                "insert_after": "stock_uom",
                "no_copy": 1,
                "read_only": 1,
            },
            {
                "label": _("Item Barcode Second"),
                "fieldname": "item_barcode",
                "fieldtype": "Barcode",
                "insert_after": "barcode",
                "no_copy": 1,
                # "read_only":1,
            },
        ],
        "Item Barcode": [
            # {
            #     "label": _("Item Barcode Child"),
            #     "fieldname": "item_barcode_child",
            #     "fieldtype": "Barcode",
            #     "insert_after": "barcode",
            #     "no_copy": 1,
            # },
        ],
    },
    "properties": [
        {
            "doctype": "Item Barcode",
            "doctype_or_field": "DocField",
            "fieldname": "barcode",
            "property": "read_only",
            "property_type": "Check",
            "value": "1",
        },
    ],
    # 'on_setup': 'dynamic.teba.setup.setup_teba'
}
