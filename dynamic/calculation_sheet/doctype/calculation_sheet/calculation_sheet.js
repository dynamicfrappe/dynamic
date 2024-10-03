// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Calculation Sheet', {
	table_gw1fd: function(frm) {
		const table_gw1fd = frm.doc.table_gw1fd ;
		if(table_gw1fd){
			let totalSellingPrice = table_gw1fd.reduce((total, item) => {
				return total + (item.unit_selling_price || 0); // If unit_selling_price is undefined, default to 0
			}, 0);
			frm.set_value("total_unit_selling_price");
			frm.refresh_field("total_unit_selling_price");
		}
	},
	equation_of_total_cost: function(frm){
		equation(frm , frm.doc.equation_of_total_cost , frm.doc.table_1 , "total_cost")
	},
	equation_of_shipping_cost: function(frm){
		equation(frm , frm.doc.equation_of_shipping_cost , frm.doc.table_1 , 'shipping_cost')
	},
	equation_of_total_selling: function(frm){
		equation(frm , frm.doc.equation_of_total_selling,frm.doc.table_1 , 'total_selling')
	},
	equation_of_gross_margin: function(frm){
		equation(frm , frm.doc.equation_of_gross_margin,frm.doc.table_1 , 'gross_margin')
	},
	equation_of_mark_up: function(frm){
		equation(frm , frm.doc.equation_of_mark_up, frm.doc.table_1 , 'mark_up')
	},
});

frappe.ui.form.on('Calculation Sheet table 2', {
	discount: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},
	quantity: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},
	list_price: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},
	additional_discound: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},
	shipping_cost: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},
	customs: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},
	additional_cost: function(frm , cdt, cdn ) {
		calculate_table_2(frm , cdt , cdn)
	},

});

function equation(frm , equation_of_total_cost , data , field_name){
	if(equation_of_total_cost){
		frappe.call({
			method: "dynamic.calculation_sheet.doctype.calculation_sheet.calculation_sheet.operations",
			args: {
				equation: equation_of_total_cost , 
				data:data,
			},
			callback: (r) => {
				console.log(r.message);
				frm.set_value(field_name , r.message);
				frm.refresh_field(field_name);
			},
		});
	}
}
function calculate_table_2 (frm , cdt , cdn){
	var child = locals[cdt][cdn] ;
	let discount = child.discount ? child.discount : 0 ;
	let quantity = child.quantity ? child.quantity : 0 ;
	let list_price = child.list_price ? child.list_price : 0 ;
	let additional_discound = child.additional_discound ? child.additional_discound : 0 ;
	let shipping_cost = child.shipping_cost ? child.shipping_cost : 0 ;
	let customs = child.customs ? child.customs : 0 ;
	let additional_cost = child.additional_cost ? child.additional_cost : 0 ;

	let total = (quantity * list_price);
	let total_first_discount = total - (total * discount / 100);
	let total_sec_discount = total_first_discount - (total_first_discount * additional_discound / 100);

	shipping_cost = ( total * shipping_cost / 100);
	customs = ( total * customs / 100);
	additional_cost = ( total * additional_cost / 100);

	let temp = total_sec_discount + shipping_cost + customs + additional_cost ;
	frappe.model.set_value(cdt , cdn , 'unit_selling_price' , temp);
}