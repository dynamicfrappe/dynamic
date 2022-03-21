// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Contract', {
    refresh: function(frm) {
        if (frm.doc.docstatus == 0) {
            console.log("from if")
            frm.add_custom_button(__("Renew"), function() {
                //console.log("renew")
                frappe.model.open_mapped_doc({
                    method: "dynamic.gebco.doctype.maintenance_contract.maintenance_contract.renew_contract",
                    frm: frm,
                });
            });
        }
    }
});