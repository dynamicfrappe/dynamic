
frappe.ui.form.on("Customer", {
    check_url: function (frm) {
        if (frm.doc.url) {
            frappe.call({
                method: "dynamic.api.get_active_domains",
                callback: function (r) {
                    if (r.message && r.message.length) {
                        if (r.message.includes("IFI")) {
                            window.open(frappe.model.scrub(frm.doc.url));
                        }
                    }
                }
            })
        }
    },
    refresh(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Terra") || r.message.includes("Elevana")) {
                        frm.add_custom_button(
                            __("Action"),
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
                    }
                }
            }
        })
    }
})