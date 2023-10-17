from frappe import _


def get_data():
	return {
		"fieldname": "preparing_the_containers",
		# "non_standard_fieldnames": {"Payment Entry": "party_name", "Bank Account": "party"},
		"transactions": [
			{"label": _("Reservation Is Approved"), "items": ["Reservation Is Approved", ]},
			
		],
	}
