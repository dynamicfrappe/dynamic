// Copyright (c) 2024, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance deposit', {
	 refresh:function(frm){
			let value = frm.doc.maintenance_deposit_value;
			let count = frm.doc.maintenance_deposit_installments_count;
			
			if (value && count) {
				let installment_amount = value / count;
				
				// Clear existing items
				frm.clear_table("maintenance_deposit_installments_items");
				
				// Calculate due dates and create rows
				for (let i = 0; i < count; i++) {
					let due_date = frappe.datetime.add_months(frm.doc.from_due, i);  // Assuming installments are monthly
					let child = frm.add_child("maintenance_deposit_installments_items", {
						due_date: due_date,
						installment_value: installment_amount
					});
				}
				
				// Refresh the table
				frm.refresh_field("maintenance_deposit_installments_items");
			} else {
				frappe.msgprint(__("Please set both Maintenance Deposit Value and Maintenance Deposit Installments Count."));
			}
	}
});
