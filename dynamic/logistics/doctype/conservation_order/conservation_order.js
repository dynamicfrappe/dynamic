// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conservation order', {
	refresh: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frappe.call({
							method:"dynamic.logistics.logistics_api.validate_items",
							callback:function(r){
								frm.fields_dict["items"].grid.get_field("item_code").get_query =
								function (doc, cdt, cdn) {
									var row = locals[cdt][cdn];
									return {
										filters: {
										'item_group': r.message,
										'is_stock_item': 1,
										}
							
									}
								};
							}
						})
						frm.fields_dict["service_items"].grid.get_field("item").get_query =
						  function (doc, cdt, cdn) {
							  var row = locals[cdt][cdn];
							  return {
								  filters: {
								  'is_stock_item': 0,
								  }
					  
							  }
						};
						// frappe.call({
						// 	method:"dynamic.logistics.logistics_api.validate_engineering_name",
						// 	callback:function(r){
						// 		frm.fields_dict["engineering_name"].grid.get_field("employee").get_query =
						// 		function (doc, cdt, cdn) {
						// 			var row = locals[cdt][cdn];
						// 			return {
						// 				filters: {
						// 				'department': r.message,
						// 				}
							
						// 			}
						// 		};
						// 	}
						// })
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
						frappe.set_route('conservation' ,'view', 'report', 'Conservation');
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
frappe.ui.form.on('Planed Item', {
	item_code: function(frm, cdt, cdn) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						var row = locals[cdt][cdn];
						frappe.call({
							method:"dynamic.logistics.logistics_api.get_item_price",
							args : {item : row.item_code},
							callback:function(r){
								row.rate = r.message
								frm.refresh_field("items")
							}
						})
					}
				}
			}
		})

	}
});

frappe.ui.form.on('Service Item', {
	item: function(frm, cdt, cdn) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						var row = locals[cdt][cdn];
						frappe.call({
							method:"dynamic.logistics.logistics_api.get_item_price",
							args : {item : row.item},
							callback:function(r){
								row.rate = r.message
								frm.refresh_field("service_items")
							}
						})
					}
				}
			}
		})

	}
});