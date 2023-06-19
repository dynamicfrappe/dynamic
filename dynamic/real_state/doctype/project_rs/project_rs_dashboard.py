



from frappe import _


def get_data():
	return {
		"fieldname": "project_name",
		"non_standard_fieldnames": {
			"Project RS Stages": "project_name",
		},
		# "internal_links": {
		# 	# "Project RS Stages": ["items", "material_request"],
		# 	# "Supplier Quotation": ["items", "supplier_quotation"],
		# 	# "Project": ["items", "project"],
		# },
		"transactions": [
			{"label": _("Stage"), "items": ["Project RS Stages"]},
		],
	}