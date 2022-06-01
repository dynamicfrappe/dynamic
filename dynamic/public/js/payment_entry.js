frappe.ui.form.on("Payment Entry", {
  setup: function (frm) {
    frm.set_query("drawn_bank_account", function () {
      return {
        filters: [
          ["bank", "=", frm.doc.drawn_bank],
          ["is_company_account", "=", 1],
        ],
      };
    });
  },
  onload(frm) {
    // your code here
    if (frm.doc.docstatus == 1 && frm.doc.cheque) {
      frm.events.add_cheque_buttons(frm);
    }
  },
  add_cheque_buttons(frm) {
    if (["New"].includes(frm.doc.cheque_status)) {
      // cheque Endorsement
      frm.add_custom_button(
        __("Endorsement"),
        function () {
          frm.events.make_cheque_endorsement(frm);
        },
        __("Cheque Management")
      );
      // Collections Cheque Now
      frm.add_custom_button(
        __("Collect Now"),
        function () {
          frm.events.collect_cheque_now(frm);
        },
        __("Cheque Management")
      );
      // deposite Cheque under collcttion 
      frm.add_custom_button(
        __("Deposit Under Collection"),
        function () {
          frm.events.deposite_cheque_under_collection(frm);
        },
        __("Cheque Management")
      );
    }
    if (["New"].includes(frm.doc.cheque_status)) {
      
    }

    // cheque under collction

    if (["Under Collect"].includes(frm.doc.cheque_status)) {
      frm.add_custom_button(
        __("Collect"),
        function () {
          frm.events.collect_cheque_under_collection(frm);
        },
        __("Cheque Under Collection")
      );
      frm.add_custom_button(
        __("Reject"),
        function () {
          frm.events.reject_cheque_under_collection(frm);
        },
        __("Cheque Under Collection")
      );
    }

    // Reject cheque under collction
    if (["Rejected in Bank"].includes(frm.doc.cheque_status)) {
      frm.add_custom_button(
        __("Reject"),
        function () {
          frm.events.reject_cheque_under_collection(frm);
        },
        __("Cheque Under Collection")
      );
    }


  },
  make_cheque_endorsement(frm) {
    if (!frm.doc.drawn_bank_account) {
      frappe.throw(__("Please Set Bank Account"));
    }
    frappe.call({
      method: "dynamic.cheques.doctype.cheque.cheque.make_cheque_endorsement",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  collect_cheque_now(frm) {
    frappe.call({
      method: "dynamic.cheques.doctype.cheque.cheque.collect_cheque_now",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  deposite_cheque_under_collection(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.deposite_cheque_under_collection",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  collect_cheque_under_collection(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.collect_cheque_under_collection",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
  reject_cheque_under_collection(frm) {
    frappe.call({
      method:
        "dynamic.cheques.doctype.cheque.cheque.reject_cheque_under_collection",
      args: {
        payment_entry: frm.doc.name,
      },
      callback: function (r) {
        frm.refresh();
        if (r && r.message) {
          frappe.set_route("Form", r.message.doctype, r.message.name);
        }
      },
    });
  },
});
