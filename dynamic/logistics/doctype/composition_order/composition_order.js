// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Composition Order', {
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
	refresh: function(frm){
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
						frappe.call({
							method:"dynamic.logistics.logistics_api.validate_engineering_name",
							callback:function(r){
								frm.fields_dict["engineers"].grid.get_field("employee").get_query =
								function (doc, cdt, cdn) {
									var row = locals[cdt][cdn];
									return {
										filters: {
										'department': r.message,
										}
							
									}
								};
							}
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
