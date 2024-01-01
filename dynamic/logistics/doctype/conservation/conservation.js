// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conservation', {
	refresh: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						if (frm.doc.docstatus == 1){
							frm.add_custom_button(__("Create Sales Invoice"),()=>{
								frappe.model.open_mapped_doc({
									method:
									"dynamic.logistics.logistics_api.create_sales_invoice",
									frm: frm,
								  });
							})
						}
					}
				}
			}
		})
	}
});
