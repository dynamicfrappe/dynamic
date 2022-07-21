frappe.ui.form.on("Payment Entry", {
  setup: function (frm) {
    frm.set_query("drawn_bank_account", function () {
      return {
        filters: [
          // ["bank", "=", frm.doc.drawn_bank],
          ["is_company_account", "=", 1],
        ],
      };
    });
    frm.set_query("endorsed_party_account", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          ["disabled", "=", 0],
        ],
      };
    });
  },
  get_party_account: function (frm, callback) {
    if (
      frm.doc.company &&
      frm.doc.endorsed_party_type &&
      frm.doc.endorsed_party_name
    ) {
      frappe.call({
        method: "erpnext.accounts.party.get_party_account",
        args: {
          party_type: frm.doc.party_type,
          party: frm.doc.party,
          company: frm.doc.company,
        },
        callback: (response) => {
          if (response) callback(response);
        },
      });
    }
  },
  endorsed_party_name: function (frm) {
    frm.events.get_party_account(frm, function (r) {
      if (r.message) {
        frm.set_value("endorsed_party_account", r.message);
      }
    });
  },
  refresh(frm) {
    // your code here
    if (frm.doc.docstatus == 1 && frm.doc.cheque) {
      frm.events.add_cheque_buttons(frm);
    }
  },
  add_cheque_buttons(frm) {
    if (frm.doc.payment_type == "Pay") {
      
    }
    if (frm.doc.payment_type == "Receive") {
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
        // deposite Cheque under collcttion
        frm.add_custom_button(
          __("Deposit Under Collection"),
          function () {
            frm.events.deposite_cheque_under_collection(frm);
          },
          __("Cheque Management")
        );
      }
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
