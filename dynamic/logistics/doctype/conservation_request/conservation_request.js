// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conservation Request', {
	customer: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.fields_dict["warranties"].grid.get_field("serial_number").get_query =
						function (doc, cdt, cdn) {
							var row = locals[cdt][cdn];
							return {
								filters: {
								'customer': frm.doc.customer,
								}
					   
							}
						};
					}
				}
			}
		})
	},
	history_maintenance : function(frm){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frappe.set_route("query-report", "Conservation Request");
					}
				}
			}
		})
	} 
});
frappe.ui.form.on('Maintenance Warranty', {
	serial_number: function(frm, cdt, cdn) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						var row = locals[cdt][cdn];
						frm.call({
							doc :frm.doc,
							args : {serial_number : row.serial_number},
							method : "get_warranties" ,
							callback:function(r){
								row.item_code = r.message[0]
								row.name1 = r.message[1]
								row.description = r.message[2]
								row.warranty = r.message[3]

								frm.refresh_field("warranties")
							}
							
						})
					}
				}
			}
		})

	}
});
