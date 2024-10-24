// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Techincal Offer', {
	refresh: function(frm) {
		frm.events.terms_and_conditions(frm)
		frm.events.general_note(frm)
	},
	terms_and_conditions:function(frm){
		const terms_and_condintions = frm.doc.commercial_offer_terms_and_condintions ;
		console.log(terms_and_condintions);
		
		if (!terms_and_condintions){
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Offer Validuty',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Currency',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Payment Terms',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Delivery Period',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Place of delivery ',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Warranty',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Taxes',
			});
			frm.add_child('commercial_offer_terms_and_condintions', {
				terms_and_condintions: 'Notes',
			});
			frm.refresh_field('commercial_offer_terms_and_condintions');


		}
	},
	general_note:function(frm){
		let general = `<div class="ql-editor read-mode"><ol><li data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>General:</font></li><li class="ql-indent-1" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>Project Purpose</font></li><li class="ql-indent-2" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>The objective of this proposal is to supply the list of materials below.</font></li><li class="ql-indent-1" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>Measurement Units and Language</font></li><li class="ql-indent-2" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>Generally, technical details are based on the metric system unless stated otherwise. The language of all documentation will be English unless stated otherwise.</font></li><li class="ql-indent-1" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>Documentation standards and samples</font></li><li class="ql-indent-2" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>Our engineering and Service performances as well as our system deliveries correspond with internationally usual high standards as well as matching with requirements/standards our final customer. </font></li><li class="ql-indent-1" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><font>Technical References:</font></li><li class="ql-indent-2" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><span style="background-color: rgb(255, 255, 255);"><font>The Equipment and parts specified in this proposal are based on the tender documents and all received relevant documents as follows:</font></span></li><li class="ql-indent-2" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><span style="background-color: rgb(255, 255, 255);"><font>Tender Specs.</font></span></li><li class="ql-indent-2" data-list="ordered"><span class="ql-ui" contenteditable="false"></span><span style="background-color: rgb(255, 255, 255);"><font><span class="ql-cursor">﻿</span>SLD.</font></span></li></ol><p><br></p></div>`
		frm.set_value("general",general);
		frm.refresh_field("general");
	},
});
