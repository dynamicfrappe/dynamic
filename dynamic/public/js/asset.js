
frappe.ui.form.on('Asset', {
    refresh(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Elhamd")) {
                        if (frm.doc.docstatus != 0){
                            frappe.call({
                                method: "dynamic.dynamic.validation.after_insert_journal_entry",
                                args :{
                                    "doc" : frm.doc.name
                                }, callback: function (res) {
                                    if (res.message) { 
                                        frm.set_value("num_journal_entry", res.message);
                                    }
                                },
                            })
                        }
                    }
                }
            }
        })
    }
});

