frappe.ui.form.on("Sales Order", {
  // validate: function(frm) {
  //   console.log('validate1111111111111111')
  //   frappe.call({
  //     method: "dynamic.api.check_source_item",
  //     args:{
  //       self:frm.doc,
  //     },
  //     callback: function(r) {
  //      console.log(r.message)
  //     }
  // });
  // },
  setup(frm) {
    frm.custom_make_buttons = {
      "Installation Request": "Installation Request",
      "Cheque": "Cheque",
    };
  },
  refresh: function (frm) {
    frm.events.add_cheque_button(frm);
    frm.events.add_installation_button(frm);
    // console.log("over Write ");
  },
  onload: function (frm) {
    // console.log("over Write ");
    // frm.set_query('item_purchase_order', 'items', function() {
		// 	return {
		// 		'filters': {
		// 			'{{ field in linked doctype }}': ['{{ operator }}', '{{ value }}']
		// 		}
		// 	};
		// });
  },
  comparison: function (frm) {
    // console.log("com");
    frappe.call({
      method: "dynamic.contracting.global_data.get_comparison_data",
      args: { comparison: frm.doc.comparison },
      callback: function (r) {
        if (r.message) {
          console.log(r.message);
          var data = r.message;
          // Set customer from comparison
          frm.doc.customer = data.customer;
          frm.refresh_field("customer");

          // set insurance from comparison

          frm.doc.down_payment_insurance_rate = data.insurance;
          frm.doc.payment_of_insurance_copy = data.d_insurance;
          frm.refresh_field("down_payment_insurance_rate");
          frm.refresh_field("payment_of_insurance_copy");

          // set sales order items
          var i = 0;
          frm.clear_table("items");
          frm.refresh_field("items");
          for (i = 0; i < data.items.length; i++) {
            var row = frm.add_child("items");
            row.item_code = data.items[i].item_code;
            row.item_name = data.items[i].item_name;
            row.description = data.items[i].description;
            row.uom = data.items[i].uom;
            row.qty = data.items[i].current_qty;
            row.rate = data.items[i].price;
            row.amount = data.items[i].amount;
          }
          frm.refresh_field("items");
        } else {
          frappe.throw("Comparison Data Error !");
        }
      },
    });
  },
  is_contracting: function (frm) {
    if (frm.doc.is_contracting == 0) {
      frm.doc.comparison = "";
      frm.refresh_field("comparison");
      frm.doc.customer = " ";
      frm.refresh_field("customer");
      frm.clear_table("items");
      frm.refresh_field("items");
      frm.doc.down_payment_insurance_rate = 0;
      frm.doc.payment_of_insurance_copy = 0;
      frm.refresh_field("down_payment_insurance_rate");
      frm.refresh_field("payment_of_insurance_copy");
    }
  },
  total_cars: function (frm) {
    if (frm.doc.total_cars) {
      frm.set_value("pending_cars", frm.doc.total_cars);
      frm.set_value("not_requested_cars", frm.doc.total_cars);
    }
  },
  set_contracting(frm) {
    frappe.call({
      method: "dynamic.contracting.global_data.get_comparison_data",
      args: { comparison: frm.doc.comparison },
      callback: function (r) {
        if (r.message) {
          console.log(r.message);
          var data = r.message;
          // Set customer from comparison
          frm.doc.customer = data.customer;
          frm.refresh_field("customer");

          // set insurance from comparison

          frm.doc.down_payment_insurance_rate = data.insurance;
          frm.doc.payment_of_insurance_copy = data.d_insurance;
          frm.refresh_field("down_payment_insurance_rate");
          frm.refresh_field("payment_of_insurance_copy");

          // set sales order items
          var i = 0;
          frm.clear_table("items");
          frm.refresh_field("items");
          for (i = 0; i < data.items.length; i++) {
            var row = frm.add_child("items");
            row.item_code = data.items[i].item_code;
            row.item_name = data.items[i].item_name;
            row.description = data.items[i].description;
            row.uom = data.items[i].uom;
            row.qty = data.items[i].current_qty;
            row.rate = data.items[i].price;
            row.amount = data.items[i].amount;
          }
          frm.refresh_field("items");
        } else {
          frappe.throw("Comparison Data Error !");
        }
      },
    });
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
  add_installation_button(frm) {
    if (frm.doc.docstatus == 1) {
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
          if (r.message && r.message.length) {
            if (r.message.includes("Gebco")) {
              frm.add_custom_button(
                __("Installation Request"),
                function () {
                  frm.events.make_installation_request(frm);
                },
                __("Create")
              );
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
  make_installation_request(frm) {
    frappe.model.open_mapped_doc({
      // installation_request_doc
      method: "dynamic.gebco.api.create_installation_request",
      frm: frm,
      // args: {
      //   total_cars: frm.doc.total_cars,
      //   sales_order: frm.doc.name,
      // },
    });
    // return frappe.call({
    //   method: "dynamic.gebco.api.create_installation_request",
    //   args: {
    //     total_cars: frm.doc.total_cars,
    //     sales_order: frm.doc.name,
    //   },
    //   callback: function (r) {
    //     console.log(r,message)
    // //     // frappe.model.open_mapped_doc({
    // //     //   // installation_request_doc
    // //     // })
    //   },
    // });
  },
  set_warehouse: function (frm) {
    frm.events.autofill_warehouse(
      frm,
      frm.doc.items,
      "item_warehouse",
      frm.doc.set_warehouse
    );
  },
  purchase_order: function (frm) {
    frm.events.autofill_purchase_order(
      frm,
      frm.doc.items,
      "item_purchase_order",
      frm.doc.purchase_order
    );
  },
  autofill_warehouse: function (frm, child_table, warehouse_field, warehouse) {
    if (warehouse && child_table && child_table.length) {
      let doctype = child_table[0].doctype;
      $.each(child_table || [], function (i, item) {
        frappe.model.set_value(doctype, item.name, warehouse_field, warehouse);
      });
    }
  },
  autofill_purchase_order: function (
    frm,
    child_table,
    warehouse_field,
    warehouse
  ) {
    if (warehouse && child_table && child_table.length) {
      let doctype = child_table[0].doctype;
      $.each(child_table || [], function (i, item) {
        frappe.model.set_value(doctype, item.name, warehouse_field, warehouse);
      });
    }
  },
});

frappe.ui.form.on("Sales Order Item", {
  item_warehouse: function (frm, cdt, cdn) {
    var row = frappe.get_doc(cdt, cdn);
    frappe.model.set_value(cdt, cdn, "warehouse", row.item_warehouse);
  },
});

frappe.ui.form.on(
  "Sales Order Item",
  "item_purchase_order",
  function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.item_purchase_order && row.item_code) {
      frappe.call({
        method: "dynamic.api.check_delivery_warehosue",
        args: {
          doc_name: row.item_purchase_order,
          item_code: row.item_code,
          warehouse: row.warehouse,
        },
        callback: function (r) {
          if (r.message){
            console.log('warehouse -> ',r.message)
            row.warehouse = r.message;
            frm.refresh_fields();
          }
        },
      });
    }
  }
);
