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
	},
	calc_deductions:(frm)=>{
		let totals = 0
		let deduct_table = frm.doc.deductions
		for(let i=0;i<deduct_table.length;i++){
			totals += deduct_table[0].amount
		}
		frm.set_value("total_deductions",totals)
		frm.refresh_field("total_deductions")
	},
	calc_total:(frm,cdt,cdn)=>{
		let row = locals[cdt][cdn]
		let total_price = row.current_qty * row.price
		row.total_price = !isNaN(total_price) ? total_price : 0
		frm.refresh_fields("items")
	}
});
frappe.ui.form.on('Deductions clearence Table', {
	amount:(frm,cdt,cdn)=>{
		frm.events.calc_deductions(frm);

	},
	deductions_remove:(frm,cdt,cdn)=>{
		frm.events.calc_deductions(frm);
	}
})
frappe.ui.form.on('Clearance Items', {
	current_qty:(frm,cdt,cdn)=>{
		frm.events.calc_total(frm,cdt,cdn)
	},
	price:(frm,cdt,cdn)=>{
		frm.events.calc_total(frm,cdt,cdn)
	}
})