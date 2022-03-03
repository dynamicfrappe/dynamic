// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on("Clearance", {
  setup(frm) {
    frm.fields_dict["items"].grid.get_field("clearance_state").get_query =
      function (doc, cdt, cdn) {
        return {
          query:
            "dynamic.contracting.doctype.clearance.clearance.get_state_query",
          filters: { parent: doc.tender },
        };
      };
    frm.set_query("account_head", "item_tax", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
          [
            "account_type",
            "in",
            [
              "Tax",
              "Chargeable",
              "Income Account",
              "Expenses Included In Valuation",
            ],
          ],
        ],
      };
    });
    frm.set_query("cost_center", "item_tax", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
        ],
      };
    });
    frm.set_query("account", "deductions", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
        ],
      };
    });

    frm.set_query("cost_center", "deductions", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
        ],
      };
    });

    frm.set_query("cost_center", "items", function () {
      return {
        filters: [
          ["company", "=", frm.doc.company],
          ["is_group", "=", 0],
        ],
      };
    });
  },
  refresh: (frm) => {
    if (frm.doc.docstatus == 1) {
      if (!frm.doc.paid) {
        frm.add_custom_button(
          __("Payment Entry"),
          function () {
            frappe.call({
              method: "create_payment_entry",
              doc: frm.doc,
            });
          },
          __("Create")
        );
      }

      if (frm.doc.clearance_type == "incoming") {
        frm.call({
          method: "can_create_invoice",
          doc: frm.doc,
          args: {
            doctype: "Purchase Invoice",
          },
          callback: function (r) {
            if (r.message) {
              frm.add_custom_button(
                __("Purchase Invoice"),
                function () {
                  frappe.model.open_mapped_doc({
                    method:
                      "dynamic.contracting.doctype.clearance.clearance.clearance_make_purchase_invoice",
                    frm: frm,
                  });
                },
                __("Create")
              );
            }
          },
        });
      }
      if (frm.doc.clearance_type == "Outcoming") {
        frm.call({
          method: "can_create_invoice",
          doc: frm.doc,
          args: {
            doctype: "Sales Invoice",
          },
          callback: function (r) {
            if (r.message) {
              frm.add_custom_button(
                __("Sales Invoice"),
                function () {
                  frappe.model.open_mapped_doc({
                    method:
                      "dynamic.contracting.doctype.clearance.clearance.clearance_make_sales_invoice",
                    frm: frm,
                  });
                },
                __("Create")
              );
            }
          },
        });
      }
    }
  },
  onload(frm) {
    if (frm.is_new()) {
      (frm.doc.items || []).forEach((row) => {
        frm.events.calc_total(frm, row.doctype, row.name);
      });
      frm.events.clac_taxes(frm);
    }
  },
  validate: (frm) => {
    frm.events.clac_taxes(frm);
  },
  comparison: (frm) => {
    let comparison = frm.doc.comparison;
    if (comparison) {
      frappe.call({
        method: "frappe.client.get",
        args: {
          doctype: "Comparison",
          name: comparison,
        },
        callback: function (r) {
          if (r.message) {
            frm.set_value(
              "down_payment_insurance_rate_",
              r.message.insurance_value_rate
            );
            frm.set_value(
              "payment_of_insurance_copy_of_operation_and_initial_delivery",
              r.message.delevery_insurance_value_rate_
            );
            frm.refresh_field("down_payment_insurance_rate_");
            frm.refresh_field(
              "payment_of_insurance_copy_of_operation_and_initial_delivery"
            );
          }
        },
      });
    }
  },
  sales_order: function (frm) {
    frappe.call({
      method: "dynamic.contracting.global_data.get_sales_order_data",
      args: {
        order: frm.doc.sales_order,
      },
      callback: function (r) {
        if (r.message) {
          console.log("done");
        } else {
          frappe.throw(" Sales Order Data Erro");
        }
      },
    });
  },
  purchase_taxes_and_charges_template: (frm) => {
    let tax_temp = frm.doc.purchase_taxes_and_charges_template;
    if (tax_temp != null) {
      frappe.call({
        method: "frappe.client.get",
        args: {
          doctype: "Purchase Taxes and Charges Template",
          name: tax_temp,
        },
        callback: function (r) {
          if (r.message) {
            let taxes = r.message["taxes"];
            //console.log("rrrrrrrrrr",taxes)
            for (let i = 0; i < taxes.length; i++) {
              let row = cur_frm.add_child("item_tax");
              row.charge_type = taxes[i].charge_type;
              row.account_head = taxes[i].account_head;
              row.rate = taxes[i].rate;
              row.tax_amount = (taxes[i].rate / 100) * frm.doc.total_price || 0;
              row.total =
                (taxes[i].rate / 100) * frm.doc.total_price +
                  frm.doc.grand_total || 0;
              row.description = taxes[i].description;
            }
            cur_frm.refresh_fields("item_tax");
            frm.events.clac_taxes(frm);
          }
        },
      });
    }
  },
  calc_deductions: (frm) => {
    console.log("frm ded action");
    let totals = 0;
    let deduct_table = frm.doc.deductions;
    let items = frm.doc.items;
    let total_items = 0;
    let total_paid_amount = 0;
    for (let i = 0; i < deduct_table.length; i++) {
      totals += deduct_table[i].amount;
    }
    for (let i = 0; i < items.length; i++) {
      total_items += items[i].total_price || 0;
    }
    total_paid_amount = total_items - totals;
    frm.set_value("total_deductions", totals);
    frm.set_value("total_payed_amount", total_paid_amount);
    frm.refresh_field("total_deductions");
    frm.refresh_field("total_payed_amount");
    frm.events.clac_taxes(frm);
  },
  calc_total: (frm, cdt, cdn) => {
    let row = locals[cdt][cdn];
    row.current_price = (row.price * (row.state_percent || 0)) / 100;
    let total_price = row.current_qty * row.current_price;
    let current_percent = (row.current_qty / row.qty) * 100;
    let current_amount = row.current_qty * row.current_price;
    let completed_qty = row.current_qty || 0 + row.previous_qty || 0;
    row.total_price = !isNaN(total_price) ? total_price : 0;
    row.current_percent = !isNaN(current_percent) ? current_percent : 0;
    row.current_amount = !isNaN(current_amount) ? current_amount : 0;
    row.completed_qty = !isNaN(completed_qty) ? completed_qty : 0;
    row.completed_percent = (row.completed_qty / row.qty) * 100;
    // calc complated

    frm.refresh_fields("items");
  },
  clac_taxes: (frm) => {
    let items = frm.doc.items || [];
    let taxes = frm.doc.item_tax || [];
    let totals = 0;
    let total_qty = 0;
    let totals_after_tax = 0;
    let total_tax_rate = 0;
    let total_tax = 0;
    let tax_table = [];
    let total_paid_amount = 0;
    for (let i = 0; i < items.length; i++) {
      totals += parseFloat(items[i].total_price || 0);
      total_qty += parseInt(items[i].current_qty || 0);
    }

    let tax_v = parseFloat(totals || 0);
    for (let i = 0; i < taxes.length; i++) {
      total_tax_rate += taxes[i].rate;
      taxes[i].tax_amount = (taxes[i].rate / 100) * totals;
      tax_v += parseFloat(taxes[i].tax_amount);
      if (i == 0) {
        taxes[i].total = tax_v;
      } else {
        taxes[i].total = tax_v;
      }
      tax_table.push(taxes[i]);
    }

    total_tax = totals * (total_tax_rate / 100);
    totals_after_tax = parseFloat(totals) + parseFloat(total_tax);
    total_paid_amount = totals_after_tax - (frm.doc.total_deductions || 0);
    //////  clear child table and add row from scratch to update amount value
    cur_frm.clear_table("item_tax");
    for (let i = 0; i < tax_table.length; i++) {
      let row = cur_frm.add_child("item_tax");
      row.charge_type = tax_table[i].charge_type;
      row.account_head = tax_table[i].account_head;
      row.rate = tax_table[i].rate;
      row.tax_amount = tax_table[i].tax_amount;
      row.total = tax_table[i].total;
    }
    //////////////// update down payment and payment insurance
    let down_payment_insurance =
      totals_after_tax * (frm.doc.down_payment_insurance_rate_ / 100);
    let payment_ins =
      totals_after_tax *
      (frm.doc.payment_of_insurance_copy_of_operation_and_initial_delivery /
        100);

    frm.refresh_fields("item_tax");
    frm.set_value("total_qty", parseFloat(total_qty));
    frm.set_value(
      "total_price",
      parseFloat(totals - (frm.doc.total_deductions || 0))
    );
    frm.set_value("tax_total", parseFloat(total_tax));
    frm.set_value("grand_total", parseFloat(total_paid_amount));
    frm.set_value("total_payed_amount", total_paid_amount);
    frm.set_value("down_payment_insurance_amount", down_payment_insurance);
    frm.set_value("payment_insurance", payment_ins);
    frm.refresh_field("total_qty");
    frm.refresh_field("total_price");
    frm.refresh_field("tax_total");
    frm.refresh_field("grand_total");
    frm.refresh_field("total_payed_amount");
    frm.refresh_field("down_payment_insurance_amount");
    frm.refresh_field("payment_insurance");
  },
  get_item_price(frm, cdt, cdn) {
    var item = locals[cdt][cdn];
    if (
      item.clearance_item &&
      item.clearance_state &&
      frm.doc.comparison &&
      frm.doc.tender
    ) {
      frappe.call({
        method:
          "dynamic.contracting.doctype.clearance.clearance.get_item_price",
        args: {
          comparison: frm.doc.comparison,
          item_code: item.clearance_item,
          clearance_state: item.clearance_state,
          qty: item.current_qty || 0,
        },
        callback: function (r) {
          if (r.message) {
            item.state_percent = r.message.state_percent || 100;
            // item.current_price = r.message.item_price || 0;
            item.price = r.message.item_price;
            frm.events.calc_total(frm, cdt, cdn);
            frm.events.clac_taxes(frm);
          }
        },
      });
    }
  },
});
frappe.ui.form.on("Deductions clearence Table", {
  amount: (frm, cdt, cdn) => {
    frm.events.calc_deductions(frm);
  },
  deductions_remove: (frm, cdt, cdn) => {
    frm.events.calc_deductions(frm);
  },
});
frappe.ui.form.on("Clearance Items", {
  current_qty: (frm, cdt, cdn) => {
    frm.events.calc_total(frm, cdt, cdn);
    frm.events.clac_taxes(frm);
  },
  price: (frm, cdt, cdn) => {
    frm.events.calc_total(frm, cdt, cdn);
    frm.events.clac_taxes(frm);
  },
  clearance_state: (frm, cdt, cdn) => {
    frm.events.get_item_price(frm, cdt, cdn);
  },
  clearance_item: (frm, cdt, cdn) => {
    frm.events.get_item_price(frm, cdt, cdn);
  },
});
frappe.ui.form.on("Purchase Taxes and Charges Clearances", {
  rate: (frm, cdt, cdn) => {
    frm.events.clac_taxes(frm);
  },
  taxes_remove: (frm, cdt, cdn) => {
    frm.events.clac_taxes(frm);
  },
  taxes_add: (frm, cdt, cdn) => {
    var row = locals[cdt][cdn];
    if (row.rate) {
      frm.events.clac_taxes(frm);
    }
  },
});
