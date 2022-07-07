frappe.ui.form.on("Sales Invoice", {
  domian_valid: function (frm) {
    var tera = false;
    frappe.call({
      method: "dynamic.dynamic.validation.get_active_domain_gebco",
      async: false,
      callback: function (r) {
        if (r.message) {
          tera = true;
        } else {
          tera = false;
        }
      },
    });
    return tera;
  },
  onload(frm) {
    var check_domain = frm.events.domian_valid();
    // console.log(check_domain)
    if (check_domain && frm.doc.docstatus == 0) {
      frm.add_custom_button(
        __("view Item Shortage"),
        function () {
          frappe.call({
            method: "dynamic.api.validate_active_domains_invocie",
            args: {
              doc: frm.doc.name,
            },
            callback: function (r) {
              console.log(r.message);
            },
          });
        },
        "view Item Shortage"
      );
    }
  },

  refresh(frm) {
    var check_domain = frm.events.domian_valid();
    if (check_domain && frm.doc.docstatus == 0) {
      frm.add_custom_button(
        __("view Item Shortage"),
        function () {
          frappe.call({
            method: "dynamic.api.validate_active_domains_invocie",
            args: {
              doc: frm.doc.name,
            },
            callback: function (r) {
              console.log(r.message);
            },
          });
        },
        "view Item Shortage"
      );
    }
  },

  validate(frm) {},

  add_cheque_button(frm) {
    if (frm.doc.docstatus == 1) {
      frm.add_custom_button(__("Cheque"), function () {
        frm.events.make_cheque_doc(frm)
      }, __("Create"));
    }
  },
  make_cheque_doc(frm){
    
  }
});
