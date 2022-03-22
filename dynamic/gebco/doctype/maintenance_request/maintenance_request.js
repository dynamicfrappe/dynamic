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
    }
});