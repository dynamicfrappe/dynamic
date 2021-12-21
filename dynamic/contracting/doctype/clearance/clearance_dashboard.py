from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'fieldname': 'clearance',
		'non_standard_fieldnames': {
			'Journal Entry': 'reference_name',
		},

		'transactions': [
			{
				'label': _('Selling'),
				'items': ['Sales Invoice']
			},
			{
				'label': _('Purchasing'),
				'items': ['Purchase Invoice']
			},
			{
				'label': _('Journal Entry'),
				'items': ['Journal Entry']
			},
		]
	}
