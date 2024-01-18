// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('PO Container', {
	refresh: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.events.set_queries(frm);
						if(frm.doc.docstatus == 1 && frm.doc.status == "Ordered"){
							frm.add_custom_button('Arrive',()=>{
								frm.call({
									doc: frm.doc,
									method: "change_status",
	
								})
							})	
						}
						if (frm.doc.docstatus == 1 && frm.doc.status == "Delivered"){
							frm.call({
								doc: frm.doc,
								method: "close_request_item",

							})

						}
					}
				}
			}
		})

	},
	fetch_items : function(frm){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						if(frm.doc.purchase_order_containers){
							frm.call({
								doc: frm.doc,
								method: "fetch_purchase_order_items",
								callback: function (r) {
								},
							});
						}
	
					}
				}
			}
		})
	},
	set_queries : function(frm){
		frm.set_query('purchase_order', 'purchase_order_containers', function(doc, cdt, cdn) {							
			return {
				filters: {
					'docstatus': 1,
					"name" :["not in",frm.doc.purchase_order_containers.map((row) => {
					  return row.purchase_order;
					}),]
				}
			}
		});
		frm.set_query('purchase_order', 'items', function(doc, cdt, cdn) {							
			return {
				filters: {
					'docstatus': 1,
					// "name" :["not in",frm.doc.items.map((row) => {
					//   return row.purchase_order;
					// }),]
				}
			}
		});
		var list	
		frm.set_query('item', 'items', function(doc, cdt, cdn) {
			var row = locals[cdt][cdn]
			if (row.purchase_order){
				frm.call({
					doc: frm.doc,
					method: "filter_items",
					args : {purchase_order : row.purchase_order},
					callback: function (r) {
						list = r.message
					},
				})
				return {
				filters: {
					"item_code" :["in", list]
				}
				}
			}
		});
	}

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
 frappe.ui.form.on("Container Item", {
	
	item: function(frm, cdt, cdn) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						var row = locals[cdt][cdn];
						if (row.item && row.purchase_order){
							frm.call({
								doc: frm.doc,
								method: "get_items_qty",
								args :{item :row.item , purchase_order : row.purchase_order},
								callback: function (r) {
									row.qty = r.message[0],
									row.row_name = r.message[1]
									frm.refresh_fields("items")
								},
							});
						}

					}
				}
			}
		})


	},
 })
 
