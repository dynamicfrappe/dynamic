frappe.ui.form.on('Customer', {
	refresh(frm) {
		// your code here
	},
    receiver_type : function(frm) {
        if (frm.doc.receiver_type) {
            frappe.meta.get_docfield("Customer",
             "receiver_id",me.frm.doc.name).reqd = (frm.doc.receiver_type=='P')
             frm.refresh_field('receiver_id')
        }
    }
})