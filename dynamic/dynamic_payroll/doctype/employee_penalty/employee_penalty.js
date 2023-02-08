// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Penalty', {
	refresh: function(frm) {
		frm.events.set_frm_query(frm)
		
	},
	set_frm_query(frm){
		frm.set_query('salary_component',function () {
			return {
			  filters: [
				["type", "=", "Deduction"],
			  ],
			};
		  })
	}
});
