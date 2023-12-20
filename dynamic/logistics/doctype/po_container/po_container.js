// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('PO Container', {
	refresh: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.fields_dict["purchase_order_containers"].grid.get_field("purchase_order").get_query =
						function (doc, cdt, cdn) {
							var row = locals[cdt][cdn];
							return {
								filters: {
								'docstatus': 1,
								'has_shipped' : 0,
								}
						
							}
						};
					}
				}
			}
		})

	},

});
frappe.ui.form.on("Purchase Order container", {
	
	purchase_order: function(frm, cdt, cdn) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						var row = locals[cdt][cdn];
						frm.call({
							doc: frm.doc,
							method: "get_purchase_order_details",
							args :{purchase_order : row.purchase_order},
							callback: function (r) {
								row.supplier = r.message[0]
								row.total = r.message[1]
								frm.refresh_fields("purchase_order_containers")
							},
							});
					}
				}
			}
		})


	},
 })
 
