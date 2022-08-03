// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Car Installation', {
	// refresh: function(frm) {

	// }
	car:function(frm){
		if(frm.doc.car){
			frappe.call({
				method: "get_car_data",
				doc: frm.doc,
				callback: function () {
			  		frm.refresh_fields();
			},
			})
		}
	}
});
