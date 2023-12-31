// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Installment Payments', {
	refresh: function(frm) {
		frm.events.add_custom_btn(frm)
		
	},
	add_custom_btn:function(frm){
		frm.add_custom_button(__("Create Journal Entry"),()=>{
			frm.call({
				method:'dynamic.alrehab.doctype.installment_payments.installment_payments.create_journal_entry',
				args:{
					doc_name:frm.doc.name
				},
				callback:function(r){
					frm.refresh_fields()
				}
			})
		},__("Create"))
	},
	fetch_installment:function(frm){
		if(frm.doc.unit){
			frm.call({
				method:"dynamic.alrehab.doctype.installment_payments.installment_payments.get_customer_instllment",
				args:{
					cst:frm.doc.unit,
					item:frm.doc.item
				},
				callback:function(r){
					if(!r.exc){
						//append childs
						frm.clear_table("items")
						console.log(r.message)
						$.each(r.message || [], function(i, element) {
							let row = frm.add_child('items', {
								installment_entry: element.name,
								total_value: element.total_value,
								total_payed: element.total_total_payed,
								delay_penalty: element.delay_penalty,
								outstanding_value: element.outstanding_value,
							
						});
						})
						frm.refresh_field("items")
					}
				}
			})
		}
	}
});
