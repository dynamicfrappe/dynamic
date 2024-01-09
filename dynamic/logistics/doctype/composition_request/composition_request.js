// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Composition Request', {
	refresh : function(frm){
		frm.set_query("sales_order", () => {
			return { filters: {"docstatus" : 1}};
		});
	},
	sales_order: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.call({
							doc : frm.doc ,
							method: "get_items",
							callback: function (r) {
								frm.doc.items = []
								r.message.forEach(element => {
									frm.add_child("items" , element);
								});
								frm.refresh_fields("items");
							},			 
						})	
					}
				}
			}
		})
	},
	customer: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.call({
							doc : frm.doc ,
							method: "set_address_and_numbers",	 
						})	
					}
				}
			}
		})
	}

});
