// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pay and Receipt Document", {
  refresh: function (frm) {
    frm.events.set_base_amount(frm);
    frm.set_query("account", function (doc) {
      return {
        filters: {
          is_group: 0,
          account_type: doc.mode_of_payment,
          company: doc.company,
        },
      };
    });
    frm.set_query("against_account", function (doc) {
      return {
        filters: {
          is_group: 0,
          // "account_type": doc.mode_of_payment ,
          company: doc.company,
        },
      };
    });
  },
  currency(frm) {
    if (frm.doc.currency) {
      frappe.call({
        method: "get_conversion_rate",
        doc: frm.doc,
        callback: function (r) {
          frm.events.set_base_amount(frm);
          frm.refresh_field("exchange_rate");
        },
      });
    }
  },
  amount(frm) {
    frm.events.set_base_amount(frm);
  },
  exchange_rate(frm) {
    frm.events.set_base_amount(frm);
  },
  set_base_amount(frm) {
    frm.doc.base_amount = 0;
    if (frm.doc.amount && frm.doc.exchange_rate) {
      frm.doc.base_amount = frm.doc.amount * frm.doc.exchange_rate;
    }
    frm.refresh_field("base_amount");
  },
});
