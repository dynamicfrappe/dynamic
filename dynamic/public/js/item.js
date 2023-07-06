

frappe.ui.form.on("Item", {
    after_save:function(frm){
        frm.refresh_fields("barcodes")
        frm.refresh_fields();
    }
})