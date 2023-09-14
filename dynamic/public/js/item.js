

frappe.ui.form.on("Item", {
    refresh:function(frm){
        // frm.refresh_fields("barcodes")
        // frm.refresh_fields();
        // frm.set_value('image',"/files/moltob1846c.png")
        frm.events.add_custom_btn(frm)
    },
    add_custom_btn:function(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Real State")) {
                        frm.add_custom_button(
                            __("Make Quotation"),
                            function () {
                              frappe.model.open_mapped_doc({
                                method:"dynamic.real_state.rs_api.create_first_contract",
                                frm: frm,
                              });
                            },
                            __("Actions")
                          );
                    }
                }
            }
        })
        
    }
})