frappe.ui.form.on("Purchase Invoice", {
  refresh: function (frm) {
    frm.custom_make_buttons["Cheque"] = "Cheque";
    frm.events.add_cheque_button(frm);
    // const myTimeout = setTimeout(get_supplier_query, 1000);

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
  cost_center(frm){
    if(frm.doc.cost_center){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
          if (r.message.includes("Qaswaa")) {
            frappe.db.get_value('Cost Center', frm.doc.cost_center, 'is_default')
              .then(r => {
                  if(r.message.is_default == 1){
                    frm.set_df_property('update_stock', 'read_only', 0);
                  }else{
                    frm.set_df_property('update_stock', 'read_only', 1);
                    frm.set_value('update_stock', 1);
                    frm.refresh_field('update_stock');
                  }
              })
            }
        }
      })
        
      }
  },
  item_discount_rate: function(frm) {
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
        if (r.message && r.message.length) {
          if (r.message.includes("Qaswaa")) {
            var item_discount_rate = frm.doc.item_discount_rate;
            frm.doc.items.forEach(function(item) {
                frappe.model.set_value(item.doctype, item.name, 'discount_percentage', item_discount_rate);
            });
            frm.refresh_field('items');
          }
        }
      },
    });
  },
});



function get_supplier_query(){
  frappe.call({
    method: "dynamic.api.get_active_domains",
    callback: function (r) {
      if (r.message && r.message.length) {
        if (r.message.includes("Master Deals")) {
          cur_frm.set_query('supplier',(doc)=>{
            return {
              query: 'dynamic.master_deals.master_deals_api.get_supplier_by_code',
              filters:{"docname":cur_frm.doc.name}
            }
            
          })
        }
      }
    },
  });
  
}