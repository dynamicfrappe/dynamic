// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Request', {
    refresh: function(frm) {
        frm.set_query('maintenance_contract', function(doc, cdt, cdn) {
            //var row = locals[cdt][cdn];
            return {
                "filters": {
                    "customer": frm.doc.company_name
                }
            };
        });
        frm.add_custom_button(__("Create Maintenance Template"), function() {
            frappe.model.open_mapped_doc({
                method: "dynamic.gebco.doctype.maintenance_request.maintenance_request.create_maintenance_request",
                frm: frm,
            });
        });
    }
});