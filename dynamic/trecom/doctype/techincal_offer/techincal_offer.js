// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Techincal Offer', {
	refresh: function(frm) {
		frm.events.terms_and_conditions(frm)
		console.log(frm.doc.general);
		console.log("frm.doc.general");
		
	},
	terms_and_conditions:function(frm){
		const terms_and_condintions = frm.doc.terms_and_condintions ;
		if (!terms_and_condintions){
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Offer Validuty',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Currency',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Payment Terms',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Delivery Period',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Place of delivery ',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Warranty',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Taxes',
			});
			frm.add_child('terms_and_condintions', {
				terms_and_condintions: 'Notes',
			});
			frm.refresh_field('terms_and_condintions');


		}
	},
});
