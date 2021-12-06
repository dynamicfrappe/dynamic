from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'fieldname': 'comparison',
		'non_standard_fieldnames': {
			'Tender': 'comparison',
			'Clearance': 'comparison',
			'Sales Order': 'comparison',
			'Purchase Order':'comparison',
			'Comparison Item Card':'comparison'
		},
		'transactions': [
			{
				'label': _('Selling'),
				'items': ['Tender', 'Clearance', 'Sales Order']
			},
			{
				'label': _('Purchasing'),
				'items': ['Purchase Order']
			},
			{
				'label': _('Stock'),
				'items': ['Comparison Item Card']
			},
		]
	}
