

frappe.ui.form.on("Supplier", {
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
                                if (r){
                                    frm.set_value('last_supplier',r.message.name)
                                    frm.refresh_field("last_supplier")
                                }
                            }
                        })
                    }
                }
            }
        })
        
    },
    check_url:function(frm){
        if(frm.doc.url){
            frappe.call({
                method: "dynamic.api.get_active_domains",
                callback: function (r) {
                  if (r.message && r.message.length) {
                    if (r.message.includes("IFI")) {
                        window.open(frappe.model.scrub(frm.doc.url));
                    }
                }}
            })
        }
    }
})