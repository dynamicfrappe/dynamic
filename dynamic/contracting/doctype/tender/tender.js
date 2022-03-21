// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tender", {
  setup(frm) {
    frm.set_query("project_account", function (doc) {
      // alert(doc.company)
      console.log("doc", doc);
      return {
        filters: {
          is_group: 0,
          company: doc.company,
        },
      };
    });
    frm.set_query("risk_insurance_account", function (doc) {
      // alert(doc.company)
      console.log("doc", doc);
      return {
        filters: {
          is_group: 0,
          company: doc.company,
          root_type:"Expense"
          // account_type:"Expense Account"
        },
      };
    });
    frm.set_query("terms_sheet_cost_center", function (doc) {
      return {
        filters: {
          is_group: 0,
          company: doc.company,
        },
      };
    });
    frm.set_query("risk_insurance_cost_center", function (doc) {
      return {
        filters: {
          is_group: 0,
          company: doc.company,
        },
      };
    });
    frm.set_query("comparison", function (doc) {
      return {
        filters: {
          docstatus: 0,
        },
      };
    });
  },
  company(frm) {},
  refresh: function (frm) {
    if (
      frm.doc.docstatus == 0 &&
      !frm.__islocal &&
      frm.doc.terms_paid == 0 &&
      frm.doc.terms_sheet_amount > 0
    ) {
      //   if (
      //     frm.doc.terms_sheet_amount > 0 &&
      //     frm.doc.current_status == "Approved"
      //   ) {
      frm.add_custom_button(
        __("Terms Sheet Payment"),
        function () {
          frappe.call({
            method: "create_terms_payment",
            doc: frm.doc,
            callback: function (r) {
              frm.refresh();
            },
          });
        },
        __("Create")
      );
      //   }
    }

    if (
      frm.doc.docstatus == 1 &&
      frm.doc.insurance_paid == 0 &&
      frm.doc.insurance_amount > 0 &&
      frm.doc.current_status == "Approved"
    ) {
      frm.add_custom_button(
        __("Insurance Payment"),
        function () {
          frappe.call({
            method: "create_insurance_payment",
            doc: frm.doc,
            callback: function (r) {
              frm.refresh();
            },
          });
        },
        __("Create")
      );
      //   }
    }
  },
  mode_of_payment(frm) {
    frappe.call({
      method: "get_payment_account",
      doc: frm.doc,
      callback: function (r) {
        frm.refresh_field("payment_account");
      },
    });
  },
  comparison: (frm) => {
    let comparison_name = frm.doc.comparison;
    if (comparison_name != null) {
      frappe.call({
        method: "frappe.client.get",
        args: {
          doctype: "Comparison",
          name: comparison_name,
        },
        callback: function (r) {
          if (r.message) {
            let obj = r.message;
            frm.set_value("insurance_rate", obj.insurance_value_rate);
            frm.set_value("insurance_amount", obj.insurance_value);
            frm.refresh_field("insurance_rate");
          }
        },
      });
    }
  },
  insurance_rate: (frm) => {
    let ins_rate = parseFloat(frm.doc.insurance_rate);
    let total_amount = parseFloat(frm.doc.total_amount);
    console.log("ins rate", ins_rate);
    console.log("total amount", total_amount);
    let amount = (ins_rate / 100) * total_amount;
    frm.set_value("insurance_amount", amount);
    frm.refresh_field("insurance_amount");
  },



current_status	:function(frm){
  if (! frm.doc.project && frm.doc.current_status =="Approved"){
    frappe.throw( "please Set Project for Approved Tender")
  }
}
});
