
frappe.ui.form.on("Opportunity", {

    refresh(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Terra")) {
                        frm.add_custom_button(
                            __("Action","Elevana"),
                            function () {
                                frappe.model.open_mapped_doc({
                                    method:
                                        "dynamic.terra.api.create_action_doc",
                                    frm: frm,
                                    args: {
                                        doctype: frm.doc.doctype,
                                    }
                                });
                            },
                            __("Create")
                        );
                        //
                       
                        // cur_frm.cscript['make_material_request'] = make_material_request
                    }
                    if (r.message.includes("IFI")) {
                        frm.remove_custom_button('Quotation','Create')
                        frm.add_custom_button(__('Quotation'),
                        function() {
                            frm.events.create_quotation(frm)
                        }, __('Create'));
                    }

                }
            }
        })
    },

    create_quotation: function(frm) {
		frappe.model.open_mapped_doc({
			method: "dynamic.ifi.api.make_quotation",
			frm: cur_frm
		})
	},
})

var make_material_request = function() {

    frappe.model.open_mapped_doc({
		method: "dynamic.terra.doctype.api.make_material_request",
		frm: cur_frm
	})
}