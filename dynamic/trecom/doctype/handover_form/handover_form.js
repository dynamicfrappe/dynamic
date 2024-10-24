// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Handover Form', {
	refresh: function(frm) {
		frm.events.po_scope_details(frm)
		
	},
	po_scope_details:function(frm){
		const po_scope = frm.doc.po_scope ;
		console.log(po_scope);
		
		const scope_data = [
			{ scope_1: 'Turn Key Project', scope_2: 'E&I' },
			{ scope_1: 'Material Supply', scope_2: 'Supervision On Installation' },
			{ scope_1: 'Service', scope_2: 'Commissioning & Start Up' },
			{ scope_1: 'Engineering', scope_2: 'Testing' },
			{ scope_1: 'Training', scope_2: 'Others Specify' }
		];

		if (po_scope.length == 0){
			scope_data.forEach(scope => {
				frm.add_child('po_scope', scope);
			});
			frm.refresh_field('po_scope');
		}
		
	},
});
