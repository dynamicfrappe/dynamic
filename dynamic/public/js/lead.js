frappe.ui.form.on("Lead", {
    check_url: function (frm) {
        if (frm.doc.url) {
            frappe.call({
                method: "dynamic.api.get_active_domains",
                callback: function (r) {
                    if (r.message && r.message.length) {
                        if (r.message.includes("IFI")) {
                            window.open(frappe.model.scrub(frm.doc.url));
                        }
                        if (r.message.includes("Terra")) {
                            frm.add_custom_button(
                                __("Action"),
                                function () {
                                    frappe.call({
                                        method: "terra.api.create_action_doc",
                                        args: {
                                            doctype: frm.doc.doctype,
                                            docname: frm.doc.name
                                        },
                                        callback: function (r) {
                                            if (r.message) {
                                                frappe.set_route("Form", r.message.doctype, r.message.name);
                                            }

                                        }
                                    });
                                },
                                __("Create")
                            ).addClass("btn-primary");
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
                    if (r.message.includes("Terra")) {
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



const LeadController_Extend = erpnext.LeadController.extend({
  
	refresh: function() {
		this._super();
        let doc = this.frm.doc;
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("IFI")) {
                        if (!this.frm.is_new() && doc.__onload && !doc.__onload.is_customer) {
                            cur_frm.page.remove_inner_button('Opportunity','Create')
                            this.frm.add_custom_button(__("Opportunity"), this.make_opportunity, __("Create"));
                        }
                    }
                }
            }
        })
        
     
	},
        make_opportunity: function () {
            frappe.model.open_mapped_doc({
                method: "dynamic.ifi.api.make_opportunity",
                frm: cur_frm
            })
        }
   
})

$.extend(
	cur_frm.cscript,
	new LeadController_Extend({frm: cur_frm}),
);

var create_ifi_sales_order = function() {

    frappe.model.open_mapped_doc({
		method: "dynamic.ifi.api.make_sales_order",
		frm: cur_frm
	})
}