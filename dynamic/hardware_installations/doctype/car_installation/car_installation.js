// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Car Installation', {
	refresh: function(frm) {

		frm.set_query("installation_order", function () {
			return {
			  filters: [
				["docstatus", "=", "1"],
			  ],
			};
		  });

		  frm.set_query("serial_number", function () {
			return {
			  filters: [
				["item_code", "=", frm.doc.gps_item_code],
				["status","=","Active"]
			  ],
			};
		  });
	},
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
	},

	installation_order:function(frm){
		if(frm.doc.installation_order){
			frappe.call({
				method: "get_cst_delgate", 
				doc: frm.doc,
				callback: function () {
			  		frm.refresh_fields();
			},
			})
		}
	},
	serial_number:function(frm){
		if(frm.doc.serial_number){
			frappe.call({
				method: "get_serial_gps", 
				doc: frm.doc,
				callback: function () {
			  		frm.refresh_fields();
			},
			})
		}
	}

});
