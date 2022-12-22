from frappe import _


def get_data():
	return {
        "fieldname": "sales_order_approval",
		"non_standard_fieldnames": {
			"Delivery Note": "sales_order_approval",
		},
        "transactions": [
			{
				"label": _("Transactions"),
				"items": ["Delivery Note"],
			},
        ]
	
	}
