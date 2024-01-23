

frappe.ui.form.on("Item", {
    setup:function(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Master Deals")) {
                        if(frm.is_new()){
                            frm.events.get_next_item_name(frm)
                           }
                    }
                }
            }
        })
         
       
    },
    refresh:function(frm){
        // frm.refresh_fields("barcodes")
        // frm.refresh_fields();
        // frm.set_value('image',"/files/moltob1846c.png")
        
        frm.events.add_custom_btn(frm)
    },
    onload: function(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Master Deals")) {
                        frappe.call({
                            method:"dynamic.master_deals.master_deals_api.get_last_doctype",
                            args:{
                                doc_type: frm.doctype
                            },
                            callback:function(r){
                                if(r){
                                    frm.set_value('next_name',r.message.name)
                                    frm.refresh_field("next_name")
                                }
                            }
                        })
                    }
                }
            }
        })
        
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
        
    },

    get_next_item_name:function(frm){
        frm.call({
            method:"dynamic.controllers.custom_item.show_next_name",
            args:{
                doc:frm.doc
            },
            callback:function(r){
                frm.set_value('next_name',r.message.new_name)
            }
        })
    },
})