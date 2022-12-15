

frappe.ui.form.on("Quotation",{
    refresh:function(frm){
        console.log(77777)
        if (frm.doc.docstatus == 1){
            cur_frm.add_custom_button(__('Payment Entry'),
					cur_frm.cscript['Make Payment Entry'], __('Create'));

        }
    }
})

cur_frm.cscript['Make Payment Entry'] = function() {
    frappe.model.open_mapped_doc({
        method:
        "dynamic.terra.api.get_payment_entry_quotation",
        frm: cur_frm,
      });
}