// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Composition Request', {
	sales_order: function(frm) {
		frm.call({
			doc : frm.doc ,
			args : {sales_order : frm.doc.sales_order},
			method: "get_items",
		})
	}
});
