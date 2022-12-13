// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Installations Furniture', {
	refresh: function(frm) {
		if (frm.doc.docstatus > 0) {
			frm.add_custom_button(
			  __("Customer Feedback"),
			  function () {
				let d = new frappe.ui.Dialog({
					title: 'Enter details',
					fields: [
						{
							label: 'Rate',
							fieldname: 'rate',
							fieldtype: 'Rating',
							reqd:1
						},
						{
							label: 'Note',
							fieldname: 'feedback',
							fieldtype: 'Small Text'
						}
					],
					primary_action_label: 'Submit',
					primary_action(values) {
						console.log(values);
						d.hide();
						frm.set_value("rate",values.rate);
						frm.set_value("feedback",values.feedback);
						frm.save()
						frm.submit()
						cur_frm.reload_doc();
					}
				});
				
				d.show();
			  }
			);
		  }
		frappe.db.get_single_value('IFI Settings','role_installation_button').then(value => {
			if(value) {{
				console.log('value-->',value)
				if (!frm.doc.__islocal &&  frappe.user.has_role(value)){
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
			}
			}}
		})
		
},
	from_time:function(frm){
		frm.events.check_date_valid(frm)
		$.each(frm.doc.items || [], function(i, d) {
			d.from_time = frm.doc.from_time;
		});
		refresh_field("items");
		// frm.events.check_exist_interval(frm)
	},
	to_time:function(frm){
		frm.events.check_date_valid(frm)
		$.each(frm.doc.items || [], function(i, d) {
			 d.to_time = frm.doc.to_time;
		});
		refresh_field("items");
	},
	change_status(frm){
		frappe.confirm('Are you sure you want to proceed?',
		() => {
			// action to perform if Yes is selected
			frm.call({
				method:"change_status",
				doc:frm.doc,
				callback:function(r){
					frm.refresh()
				}
			})
		}, () => {
			// action to perform if No is selected
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
		if(frm.doc.__islocal === 1 ){
			frappe.throw("Save First")
		}
		frm.call({
			method:"check_employee_busy",
			doc:frm.doc,
		callback:function(r){
			frm.refresh()
		}
		})
	},
	team: function (frm) {
		if (frm.doc.team) {
		  frappe.call({
			method: "get_team",
			doc: frm.doc,
			callback: function () {
			  frm.refresh_fields();
			},
		  });
		}
	  },
});
