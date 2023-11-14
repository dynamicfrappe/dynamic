

from frappe import _


def get_data():
	return {
		"fieldname": "installment_payments",
		# "non_standard_fieldnames": {
		# 	"Work Order": "production_item",
		# 	"Product Bundle": "new_item_code",
		# 	"BOM": "item",
		# 	"Batch": "item",
		# },
		"transactions": [
			# {"label": _("Installment Payments"), "items": ["Installment Payments",]},
			# {"label": _("Journal Entry"), "items": ["Journal Entry",]},
			# {"label": _("Pricing"), "items": ["Item Price", "Pricing Rule"]},
			
		],
	}
