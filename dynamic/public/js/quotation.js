

// frappe.ui.form.on("Quotation",{
//     refresh:function(frm){
//         console.log(555)
//         if (frm.doc.docstatus == 1){
//             cur_frm.add_custom_button(__('Payment Entry'),
// 					cur_frm.cscript['Make Payment Entry'], __('Create'));

//         }
//     }
// })

// cur_frm.cscript['Make Payment Entry'] = function() {
// 	frappe.call({
// 		method:
// 		"erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry_quotation",
// 		args: {
// 			dt: cur_frm.doc.doctype,
// 			dn: cur_frm.doc.name,
// 		},
// 		callback: function (r) {
// 			var doc = frappe.model.sync(r.message);
// 			frappe.set_route("Form", doc[0].doctype, doc[0].name);
// 		},
// 	})
// }