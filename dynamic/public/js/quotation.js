frappe.ui.form.on("Quotation",{
    onload:function(frm) {
        frm.events.refresh(frm)
    },
    onload:function(frm){
        console.log("over ride work")
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                
              if (r.message && r.message.length) {
                if (r.message.includes("Terra")) {
                    if (frm.doc.docstatus == 1){
                        cur_frm.add_custom_button(__('Payment Entry'),
                                cur_frm.cscript['Make Payment Entry'], __('Create'));
                    }
                }
                //? for ifi domain
               

                if (r.message.includes("IFI")) {
                    console.log('ifi')
                    if(frm.doc.docstatus == 1 && frm.doc.status!=='Lost') {
                        if(!frm.doc.valid_till || frappe.datetime.get_diff(frm.doc.valid_till,
                             frappe.datetime.get_today()) >= 0) {
                                cur_frm.page.remove_inner_button('Sales Order','Create')
                                cur_frm.add_custom_button(__('Sales Order'),
                                    cur_frm.cscript['Make Sales Order'], __('Create'));
                        }
                        cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
                    }    
                }

            }
        }
    })
    },
    onload_post_render:function(frm){
        console.log("This")
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                //? for ifi domain
                cur_frm.page.remove_inner_button('Sales Order','Create')
                if (r.message.includes("IFI")) {
                    if(frm.doc.docstatus == 1 && frm.doc.status!=='Lost') {
                        if(!frm.doc.valid_till || frappe.datetime.get_diff(frm.doc.valid_till,
                             frappe.datetime.get_today()) >= 0) {
                                cur_frm.add_custom_button(__('Sales Order'),
                                    cur_frm.cscript['Make Sales Order'], __('Create'));
                        }
                        cur_frm.page.set_inner_btn_group_as_primary(__('Create'));
                    }    
                }

            }
        }
    })

    }
})

cur_frm.cscript['Make Sales Order'] = function() {
	frappe.model.open_mapped_doc({
		method: "dynamic.ifi.api.make_sales_order",
		frm: cur_frm
	})
}

cur_frm.cscript['Make Payment Entry'] = function() {
    frappe.model.open_mapped_doc({
        method:
        "dynamic.terra.api.get_payment_entry_quotation",
        frm: cur_frm,
      });
}


<<<<<<< HEAD

//check
// const qutation_extend = erpnext.selling.QuotationController.extend({
//   refresh: function(doc, dt, dn) {
// 		var me = this;
// 		this._super(doc);
//     frappe.call({
//         method: "dynamic.api.get_active_domains",
//         callback: function (r) {
//           if (r.message && r.message.length) {
//             console.log('r',r.message)
//             if (r.message.includes("IFI")) {
//                 if(cur_frm.doc.docstatus == 1 && cur_frm.doc.status!=='Lost') {
//                     if(!cur_frm.doc.valid_till || frappe.datetime.get_diff(cur_frm.doc.valid_till,
//                          frappe.datetime.get_today()) >= 0) {
//                             cur_frm.add_custom_button(__('Sales Order'),
//                                 cur_frm.cscript['Make Sales Order'], __('Create'));
//                     }
//                 } 
                
//             }
//           }
//         }
//       })
			
//     },
// });

// // this tell current form to use this override script
// $.extend(
// 	cur_frm.cscript,
// 	new qutation_extend({frm: cur_frm}),
// );
=======
>>>>>>> b9e914455f882992c35ceecc35d6680726ed2b35
