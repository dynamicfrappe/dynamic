// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loading Doctype', {
	refresh: function(frm) {
		frm.events.add_custom_btn(frm)
	},
	add_custom_btn:function(frm){
		frm.add_custom_button(__("Create Loading Quality"),()=>{
			frappe.model.open_mapped_doc({
				method:"dynamic.nilex.nilex_api.nilex_api.quality_doc_init",
				frm: frm,
			  });
		},
		__("Create")
		)
	}
});
