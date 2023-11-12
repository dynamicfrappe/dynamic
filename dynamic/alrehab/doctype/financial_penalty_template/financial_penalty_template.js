// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Financial penalty template', {
	// refresh: function(frm) {

	// }
	auto_create:function(frm){
		frm.set_df_property("has_equation", "read_only", frm.doc.auto_create)
	},
	has_equation:function(frm){
		frm.set_df_property("auto_create", "read_only", frm.doc.has_equation)
	},
});
