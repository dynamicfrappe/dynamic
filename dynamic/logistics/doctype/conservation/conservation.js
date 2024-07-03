// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conservation', {
	refresh: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.events.add_buttons(frm)

					}
				}
			}
		})
		frm.set_query("survey", () => {
			return { filters:[["type", "=", "Maintenance"]],
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
	history_maintenance : function(frm){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frappe.set_route("query-report", "Conservation");
					}
				}
			}
		})
	},
	add_buttons : function(frm){
		if (frm.doc.docstatus == 1){
			frm.add_custom_button(__("Sales Invoice"),()=>{
				frappe.model.open_mapped_doc({
					method:
					"dynamic.logistics.logistics_api.create_sales_invoice",
					frm: frm,
				  });
			} , "Create")
		}
		if ((frm.doc.docstatus == 1) && (frm.doc.items.length > 0 )){
			frm.add_custom_button(__("Stock entry"),()=>{
				frappe.model.open_mapped_doc({
					method:
					"dynamic.logistics.logistics_api.create_stock_entry_from_conservation",
					frm: frm,
				});
			}, "Create")
	}
	}
});
