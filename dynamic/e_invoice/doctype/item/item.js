frappe.ui.form.on("Item", {
    //   refresh(frm) {
//     // your code here
//   },
  item_type(frm) {
    //   if (frm.doc.tax_auth) {
    if (frm.doc.item_type == "EGS") {
      frappe.call({
        method: "frappe.client.get",
        args: {
          doctype: "Company",
          name: frappe.defaults.get_default("company"),
        },
        callback: function (r) {
          if (r.message) {
            frm.doc.itemcode =`EGS-${r.message.tax_id||''}-${frm.doc.item_code||''}`
          }
          frm.refresh_field("itemcode");
        },
      });
    }
    frm.refresh_field("itemcode");

    //   }
  },
    onload(frm) {
      frm.events.barcode(frm);
    },
    refresh(frm) {
      frm.events.barcode(frm);
    },
    validate(frm) {
      frm.events.barcode(frm);
    },
    barcode(frm) {
      frm.doc.barcode = frm.doc.item_code;
      frm.refresh_field("barcode");
    },
});
