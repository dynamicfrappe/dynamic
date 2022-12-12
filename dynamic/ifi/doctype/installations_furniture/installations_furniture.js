// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Installations Furniture', {
	refresh: function(frm) {
		if (!frm.doc.__islocal){
			if(frm.doc.ref_status==='Pending'){
				frm.add_custom_button(__("Start"), function() {
					frm.events.change_status(frm)
			})}
			if(frm.doc.ref_status==='Start'){
				frm.add_custom_button(__("Inprogress"), function() {
					frm.events.change_status(frm)
					
			})}
			if(frm.doc.ref_status==='Inprogress'){
				frm.add_custom_button(__("Completed"), function() {
					frm.events.change_status(frm)
			})
		}
	}},
	from_time:function(frm){
		frm.events.check_date_valid(frm)
		$.each(frm.doc.items || [], function(i, d) {
			d.from_time = frm.doc.from_time;
		});
		refresh_field("items");
		frm.events.check_exist_interval(frm)
	},
	to_time:function(frm){
		frm.events.check_date_valid(frm)
		$.each(frm.doc.items || [], function(i, d) {
			 d.to_time = frm.doc.to_time;
		});
		refresh_field("items");
	},
	change_status(frm){
		frm.call({
			method:"change_status",
			doc:frm.doc,
			callback:function(r){
				frm.refresh()
			}
		})
	},
	check_date_valid(frm){
		if(frm.doc.from_time && frm.doc.to_time){
			if(frm.doc.from_time > frm.doc.to_time){
				frappe.throw(__("To Time should be greate than from time"))
			}
			// frm.events.check_exist_interval(frm)
		}
	},
	check_exist_interval(frm){
		if(frm.doc.docstatus != 0){
			frappe.throw("Save First")
		}
		frm.call({
			method:"check_employee_busy",
			doc:frm.doc,
		callback:function(r){
			frm.refresh()
		}
		})
	}
});
