// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on("Clearance", {
  refresh:(frm)=>{
    if(frm.doc.docstatus == 1 && frm.doc.paid == 0) {
      frm.add_custom_button(__('Create Payment'), function () {
        frappe.call({
          method: "create_payment_entry",
          doc:frm.doc
        })
      });
    }
  },
  onload(frm) {
    (frm.doc.items || []).forEach((row) => {
      frm.events.calc_total(frm, row.doctype, row.name);
    });
    frm.events.clac_taxes(frm);
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
  },
  calc_total: (frm, cdt, cdn) => {
    let row = locals[cdt][cdn];
    let total_price = row.current_qty * row.price;
    let current_percent = (row.current_qty / row.qty) * 100;
    let current_amount = row.current_qty * row.price;
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
    frm.set_value("total_price", parseFloat(totals));
    frm.set_value("tax_total", parseFloat(total_tax));
    frm.set_value("grand_total", parseFloat(totals_after_tax));
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
