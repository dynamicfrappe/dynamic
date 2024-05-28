from __future__ import unicode_literals
import frappe
from frappe import _

data = {
    'custom_fields':{
        
        "Item":
        [
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "item_group",
            },
        ],
        "Quotation Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "stock_qty",
                "collapsible ":1 
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item_code.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume", 
                "read_only":1,
            }
        ],
        "Sales Order Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
                "collapsible ":1 
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
            }
        ],
        "Sales Invoice Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
                
            }
        ],
        "Delivery Note Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
            }
        ],
        "Supplier Quotation Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
                
            }
        ],
        "Purchase Order Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
            }
        ],
        "Purchase Invoice Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
            }
        ],
        "Purchase Receipt Item":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
            }
        ],
        "Stock Entry Detail":
        [
            {
                "fieldname": "volume_details",
                "label": "Volume Details",
                "fieldtype": "Section Break",
                "insert_after": "item_name",
            },
            {
                "fieldname": "volume",
                "label": "Volume",
                "fieldtype": "Data",
                "insert_after": "volume_details",
                "read_only":1,
                "fetch_from": "item.volume",
            },
            {
                "fieldname": "total_volume",
                "label": "Total Volume",
                "fieldtype": "Float",
                "insert_after": "volume",
                "read_only":1,
            }
        ],
        "Quotation": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Sales Order": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Sales Invoice": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Delivery Note": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Supplier Quotation": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Purchase Order": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Purchase Invoice": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Purchase Receipt": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "total_qty",
                "read_only":1,
            }
        ],
        "Stock Entry": 
        [
            {
                "fieldname": "items_total_volume",
                "label": "Items Total Volumes",
                "fieldtype": "Float",
                "insert_after": "items",
                "read_only":1,
            }
        ],
    }
}