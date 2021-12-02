from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'fieldname': 'comparison',
		'non_standard_fieldnames': {
			'Tender': 'comparison',
			'Clearance': 'comparison',
			'Sales Order': 'comparison',
		},
		'transactions': [
			{
				'label': _('Fulfillment'),
				'items': ['Tender', 'Clearance', 'Sales Order']
			},
		]
	}
