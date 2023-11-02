// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('installment Entry', {
	refresh: function(frm) {
		frm.add_custom_button(__("calc"),()=>{
			frm.call({
				method:'caculate_installment_value',
				doc: frm.doc,
				args:{
					entry:frm.doc.name
				},
				callback:function(r){
					frm.refresh_fields()
				}
			})
		})
	}
});
