// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request Editing Item', {
	refresh: function(frm) {

		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						if(frm.doc.docstatus == 1 && frm.doc.approve_by){
							frm.add_custom_button('Create Stock Entry',()=>{
								frm.call({
									doc: frm.doc,
									method: "create_stock_entry",
									callback: function (r) {
									},
								});
							})		 
				
						}
					}
				}
			}
		})


	}
});
frappe.ui.form.on("Request Item", {
	item_code: function(frm, cdt, cdn) {
		
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						var row = locals[cdt][cdn];
						if(frm.doc.source_warehouse)
						{
							row.in_warehouse = frm.doc.source_warehouse
							frm.refresh_fields("main_item")
							frm.call({
								doc: frm.doc,
								method: "get_item_qty",
								args :{item_code : row.item_code , 
									warehouse : row.in_warehouse},
								callback: function (r) {
									if(r.message){
										row.qty = r.message
									}
									frm.refresh_fields("main_item")
								},
							});
						}
					}
				}
			}
		})




	},
 })
