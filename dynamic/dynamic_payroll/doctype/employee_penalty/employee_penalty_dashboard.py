from frappe import _


def get_data():
	return {
		"fieldname": "ref_docname",#"additional_salary",
		"non_standard_fieldnames": {
			"Additional Salary": "ref_docname",
		},
		"transactions": [
			
			{"label": _("Addtional Salary"), "items": ["Additional Salary"]},
		],
	}
