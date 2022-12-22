frappe.ui.form.on("Purchase Order", {
  refresh: function (frm) {
    frm.custom_make_buttons["Cheque"] = "Cheque";
    frm.events.add_cheque_button(frm);
    
    frm.events.get_linked_doctypes(frm)

   
  },
  
  get_linked_doctypes(frm) {
		return new Promise((resolve) => {
			if (frm.__linked_doctypes) {
				resolve();
			}

			frappe.call({
				method: "frappe.desk.form.linked_with.get_linked_doctypes",
				args: {
					doctype: frm.doc.doctype
				},
				callback: (r) => {
					frm.__linked_doctypes = r.message;
					resolve();

				}
			});
		});
	},
  add_cheque_button(frm) {
    if (frm.doc.docstatus == 1) {
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
          if (r.message && r.message.length) {
            if (r.message.includes("Cheques")) {
              if (
                frm.doc.outstanding_amount != 0 &&
                !(cint(frm.doc.is_return) && frm.doc.return_against)
              ) {
                frm.add_custom_button(
                  __("Cheque"),
                  function () {
                    frm.events.make_cheque_doc(frm);
                  },
                  __("Create")
                );
              }
            }
          }
        },
      });
    }
  },
  make_cheque_doc(frm) {
    return frappe.call({
      method: "dynamic.cheques.doctype.cheque.cheque.make_cheque_doc",
      args: {
        dt: frm.doc.doctype,
        dn: frm.doc.name,
      },
      callback: function (r) {
        var doc = frappe.model.sync(r.message);
        frappe.set_route("Form", doc[0].doctype, doc[0].name);
      },
    });
  },
});


// frappe.ui.form.on("Purchase Order", "refresh", function(frm) {
//   console.log('refresh')
//   frm.set_query("shipping_rule", function(){
//     return {
//         "filters": [
//             ["shipping_rule_type", "=", ["Selling","Buying"]],
//         ]
//     };
// });
  // frm.set_query("shipping_rule", function() {
  //     return {
  //         filters: [
  //           ["shipping_rule_type", "in", ,['Selling','Buying']],
           
  //         ],
  //     };
  // });
// });

// cur_frm.set_query("shipping_rule",function(){
//   console.log('test')
//   return{
//     "filters":{
//       "tset": "IFI"
//     }
//   };
// });
// frm.set_query("shipping_rule", function() {
//   console.log('doc ++++',doc)
//   return {
//     filters: {
//       company:frm.doc.company
//     }
//   };
// });

// frm.set_query("shipping_rule", function (doc) {
//   console.log('doc',doc)
//   return {
//     filters: [
//       ["company", "=",  frmdoc.company],
//       ["docstatus", "=", 1]
//   ],
//   };
// });