// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Preparing the containers', {
	// refresh: function(frm) {

	// }
	sales_order:function(frm){
		if(frm.doc.sales_order){
			frm.trigger("update_items_sales_order")
		}
	},
	update_items_sales_order:function(frm){
		frappe.call({
			method:"dynamic.nilex.nilex_api.nilex_api.get_sales_order_items",
			args:{
				doc_name:frm.doc.name,
				so_name:frm.doc.sales_order,
			},
			callback:function(r){
				if(!r.exc){
					$.each(r.message,function(i,d){
						let row = frm.add_child('items', {
							item_code: d.item_code,
							rate: d.rate,
							amount: d.amount,
							delivery_date: d.delivery_date,
							qty: d.qty,
							item_name: d.item_name,
							description: d.description,
							uom: d.uom,
							conversion_factor: d.conversion_factor,
						});
					})
					frm.refresh_fields("items")
				}
			}
		})
	}
});
