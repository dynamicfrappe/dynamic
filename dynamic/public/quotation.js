

erpnext.selling.QuotationController = erpnext.selling.SellingController.extend({
	refresh: function(doc, dt, dn) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("IFI")) {
                    if(doc.docstatus == 1 && doc.status!=='Lost') {
                        if(!doc.valid_till || frappe.datetime.get_diff(doc.valid_till, frappe.datetime.get_today()) >= 0) {
                            cur_frm.add_custom_button(__('Sales Order'),
                                cur_frm.cscript['Make Sales Order'], __('Create'));
                        }
                        cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
                    }    
                }
            }}
        })
    }
})

cur_frm.cscript['Make Sales Order'] = function() {
	frappe.model.open_mapped_doc({
		method: "dynamic.ifi.api.make_sales_order",
		frm: cur_frm
	})
}