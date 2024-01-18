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
								frm.fields_dict["items"].grid.get_field("item").get_query =
								function (doc, cdt, cdn) {
									var row = locals[cdt][cdn];
									return {
										filters: {
										'item_group': r.message,
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
						frappe.call({
							method:"dynamic.logistics.logistics_api.validate_engineering_name",
							callback:function(r){
								frm.fields_dict["engineering_name"].grid.get_field("employee").get_query =
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
						frappe.set_route("query-report", "Conservation Order");
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
// frappe.ui.form.on('Engineering Name', {
// 	from: function(frm, cdt, cdn) {
// 		let row = locals[cdt][cdn]
// 		frappe.call({
// 			method: "dynamic.api.get_active_domains",
// 			callback: function (r) {
// 				if (r.message && r.message.length) {
// 					if (r.message.includes("Logistics")) {
// 						// console.log("Dssssssss");
// 						// var row = locals[cdt][cdn];
// 						// frappe.call({
// 						// 	method:"dynamic.logistics.logistics_api.get_item_price",
// 						// 	args : {item : row.item},
// 						// 	callback:function(r){
// 						// 		row.rate = r.message
// 						// 		frm.refresh_field("service_items")
// 						// 	}
// 						// })
// 					}
// 				}
// 			}
// 		})

// 	}
// });
frappe.ui.form.on("Engineering Name", "to", function(frm, cdt, cdn) {
	let row = locals[cdt][cdn]
	frappe.call({
		method: "dynamic.api.get_active_domains",
		callback: function (r) {
			if (r.message && r.message.length) {
				if (r.message.includes("Logistics")) {
					if (row.employee && row.from){

						// console.log("Dssssssss"); 
						// console.log(row.employee)
						// console.log(row.from)
						// frm.call({
						// 	doc :frm.doc,
						// 	args : {employee_name : row.employee , from_time : row.from , to_time : row.to},
						// 	method : "validate_enginners" ,
						// 	callback:function(r){


						// 		// frm.refresh_field("warranties")
						// 	}
							
						// })
					}
					// var row = locals[cdt][cdn];
					// frappe.call({
					// 	method:"dynamic.logistics.logistics_api.get_item_price",
					// 	args : {item : row.item},
					// 	callback:function(r){
					// 		row.rate = r.message
					// 		frm.refresh_field("service_items")
					// 	}
					// })
				}
			}
		}
	})

});