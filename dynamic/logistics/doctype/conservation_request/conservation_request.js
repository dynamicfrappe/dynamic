// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conservation Request', {
	refresh :function(frm){
		frm.set_query("survey", () => {
			return { filters:[["type", "=", frm.doc.doctype]],
			};
		});
	},
	survey : function(frm){
		frm.call({
			doc: frm.doc,
			method: "fetch_survey_template",
			args : {survey :frm.doc.survey},
			callback: function (r) {
				
				refresh_fields("survey_template")
			},
		});
	},
	customer: function(frm) {

		frappe.db.get_value('Address', {'address_title': frm.doc.customer} , ['name'])
				.then(r => {
					console.log(r.message.name)
					frm.set_query("customer_primary_address", () => {
						return { filters:[["name", "=", r.message.name]],
						};
					});
				})

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
								console.log(r.message)
								row.item_code = r.message.item_code
								row.name1 = r.message.item_name
								row.description = r.message.description
								row.warranty = r.message.warranty_expiry_date
								row.item_name = r.message.item_name
								row.uom = r.message.uom

								frm.refresh_field("warranties")
							}
							
						})
					}
				}
			}
		})

	}
});
