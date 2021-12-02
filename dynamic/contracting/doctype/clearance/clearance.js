// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Clearance', {
	sales_order: function(frm) {
			frappe.call({
				"method" :"dynamic.contracting.global_data.get_sales_order_data", 
				"args":{
					"order":frm.doc.sales_order
				},callback:function(r){
					if (r.message){
							console.log("done")
					}
					else{
						frappe.throw(" Sales Order Data Erro")
					}
				}
			})
	}
});
