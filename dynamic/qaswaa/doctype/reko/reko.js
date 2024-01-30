// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('reko', {
	refresh: function(frm) {
		frm.add_custom_button(("test"),function(){
			frm.call({
				method:"dynamic.qaswaa.doctype.reko.reko.test",
				callback:function(r){
					console.log('test-----------')
				}
			})
		})
	}
});
