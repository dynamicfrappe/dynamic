// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Composition', {
	refresh : function(frm){
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
	status: function(frm){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.call({
							doc : frm.doc ,
							method: "update_status",
							callback: function (r) {
							},			 
						})	
					}
				}
			}
		})
	}
});
