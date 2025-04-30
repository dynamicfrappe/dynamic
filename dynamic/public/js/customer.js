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
    create_call(frm) {
        /// Work only on elevana store domain 
        frappe.call(
            {
                "method": "dynamic.elevana.api.create_call_js",
                args: {
                    "doc": "Customer",
                    "name": frm.doc.name
                }
            }
        )
    },
    refresh(frm) {
        frm.add_custom_button(
            __("New Contract"),
            function () {
                frappe.new_doc('Contract', { //on click create new contract
                    party_name: frm.doc.name  // prefill customer field
                });
            },
        );
        frm.add_custom_button(
            __("Create cst"),
            function () {
                frm.events.create_cst(frm)
            },
        );
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {

                if (r.message.includes("Elevana")) {
                    frm.add_custom_button(
                        __("Call"), function () {
                            frm.events.create_call(frm)
                        }

                    )
                }
                if (r.message.includes("True lease")) {
                    if (frm.doc.lead_name) {
                        frappe.call({
                            method: "dynamic.true_lease.api.fetch_account_manager",
                            args: {
                                lead_name: frm.doc.lead_name,
                            },
                            callback: function (r) {
                                if (r.message) {
                                    frm.set_value('account_manager', r.message[0])
                                    frm.set_value('sector', r.message[1])
                                }
                            },
                        });

                    }
                }
                if (r.message && r.message.length) {
                    if (r.message.includes("Terra") || r.message.includes("Elevana") || r.message.includes("CRM Advance")) {
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
                        frm.add_custom_button(
                            __("Appointment"),
                            function () {
                                frm.events.create_cst_appointment(frm)
                            },
                            __("Create")
                        );
                    }
                    if (r.message.includes("CRM Advance")) {
                        if (!frm.doc.__islocal) {
                            frm.add_custom_button(
                                __("Show History"),
                                function () {
                                    frappe.set_route('query-report', 'Actions Report', { "phone_no": frm.doc.phone_no })
                                }
                            );
                        }
                    }




                }
            }
        })
    },
    create_cst_appointment: function (frm) {
        frappe.model.open_mapped_doc({
            method:
                "dynamic.terra.api.create_cst_appointment",
            frm: frm,
        });
    },
    create_cst: function (frm) {
        frappe.set_route('Form', 'Customer', 'test')
        // frm.call({
        //     method:"dynamic.master_deals.master_deals_api.create_cst",
        //     args:{
        //         cst_name:frm.doc.name
        //     },
        //     callback:function(r){
        //         console.log(r.message)
        //         frappe.set_route('Form','Sales Invoice',r.message)
        //     }
        // })

    },
    onload: function (frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Master Deals")) {
                        frappe.call({
                            method: "dynamic.master_deals.master_deals_api.get_last_doctype",
                            args: {
                                doc_type: frm.doctype
                            },
                            callback: function (r) {
                                if (r) {
                                    console.log(r.message)
                                    frm.set_value('last_customer', r.message.name)
                                    frm.refresh_field("last_customer")
                                }
                            }
                        })
                    }
                }
            }
        })

    },
})