// Copyright (c) 2022, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cheque", {
	setup: function (frm) {

		frm.set_query("account_paid_from", function () {
			return {
			  filters: [
				["company", "=", frm.doc.company],
				["is_group", "=", 0],
				["disabled", "=", 0],
			  ],
			};
		  });

		  frm.set_query("account_paid_to", function () {
			  return {
				filters: [
				  ["company", "=", frm.doc.company],
				  ["is_group", "=", 0],
				  ["disabled", "=", 0],
				],
			  };
			});
	},
	refresh: function (frm) {},
	onload: function (frm) {
    if (frm.is_new()) {
      frm.events.set_new_form_date(frm);
    }
  },
  set_new_form_date: function (frm) {
    frm.doc.status = "New";
    frm.refresh_fields();
  },
  payment_type: function (frm) {
    if (!frm.doc.payment_type) return;
    frm.doc.party_type =
      frm.doc.payment_type == "Pay" ? "Supplier" : "Customer";
    frm.doc.party = "";
    frm.events.get_cheque_account(frm);
    frm.refresh_fields();
  },
  party: function (frm) {
    frm.events.get_party_account(frm, function (r) {
      if (r.message) {
        frm.set_value("account_paid_from", r.message);
      }
    });
  },
  mode_of_payment: function (frm) {
    // get_payment_mode_account(frm, frm.doc.mode_of_payment, function (account) {
    //   frm.set_value("account_paid_to", account);
    // });
  },
  get_party_account: function (frm, callback) {
    if (frm.doc.company && frm.doc.party_type && frm.doc.party) {
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
  get_cheque_account: function (frm) {
    if (!frm.doc.payment_type || !frm.doc.company) return;
    let account_name =
      frm.doc.payment_type == "Pay"
        ? "saved_cheques_bank_account"
        : "incoming_cheque_wallet_account";
    frappe.db
      .get_value("Company", frm.doc.company, account_name)
      .then((value) => {
        if (value.message) {
          frm.set_value("account_paid_to", value.message[account_name]);
          frm.refresh_field("account_paid_to");
        }
      });
  },
});

var get_payment_mode_account = function (frm, mode_of_payment, callback) {
  if (!frm.doc.company) {
    frappe.throw({
      message: __("Please select a Company first."),
      title: __("Mandatory"),
    });
  }

  if (!mode_of_payment) {
    return;
  }

  return frappe.call({
    method:
      "erpnext.accounts.doctype.sales_invoice.sales_invoice.get_bank_cash_account",
    args: {
      mode_of_payment: mode_of_payment,
      company: frm.doc.company,
    },
    callback: function (r, rt) {
      if (r.message) {
        callback(r.message.account);
      }
    },
  });
};
