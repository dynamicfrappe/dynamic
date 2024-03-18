frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {
        frm.add_custom_button(__('Sales Invoice'),
			function() {
				if (!frm.doc.customer) {
					frappe.throw({
						title: __("Mandatory"),
						message: __("Please Select a Customer")
					});
				}
				erpnext.utils.map_current_doc({
					method: "dynamic.qaswaa.controllers.delievery_note.make_delivery_note",
					source_doctype: "Sales Invoice",
					target: frm,
					setters: {
						customer: frm.doc.customer,
					},
					get_query_filters: {
						docstatus: 1,
						status: ["not in", ["Closed", "On Hold"]],
						// per_delivered: ["<", 99.99],
						company: frm.doc.company,
						project: frm.doc.project || undefined,
					}
				})
			}, __("Get Items From"));
    }
});
