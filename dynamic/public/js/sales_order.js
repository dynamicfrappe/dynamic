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
    frm.events.add_furniture_installation_button(frm);
    cur_frm.page.remove_inner_button(__('Update Items'))
    if(frm.doc.docstatus === 1 && frm.doc.status !== 'Closed'
			&& flt(frm.doc.per_delivered, 6) < 100 && flt(frm.doc.per_billed, 6) < 100) {
			frm.add_custom_button(__('Update Items'), () => {
        erpnext.utils.update_child_items({
					frm: frm,
					child_docname: "items",
					child_doctype: "Sales Order Detail",
					cannot_add_row: true,
				})
			});
		}
 
    // frm.events.domian_valid()
  },
  onload: function (frm) {
    // console.log("over Write ");
    frm.set_query('item_purchase_order', 'items', function(doc, cdt, cdn) {
      let row = locals[cdt][cdn];
			return {
				query: 'dynamic.api.get_purchase_order',
				filters:{"item_code":row.item_code}
			};
		});
  },
  // comparison: function (frm) {
  //   // console.log("com");
  //   frappe.call({
  //     method: "dynamic.contracting.global_data.get_comparison_data",
  //     args: { comparison: frm.doc.comparison },
  //     callback: function (r) {
  //       if (r.message) {
  //         console.log(r.message);
  //         var data = r.message;
  //         // Set customer from comparison
  //         frm.doc.customer = data.customer;
  //         frm.refresh_field("customer");

  //         // set insurance from comparison

  //         frm.doc.down_payment_insurance_rate = data.insurance;
  //         frm.doc.payment_of_insurance_copy = data.d_insurance;
  //         frm.refresh_field("down_payment_insurance_rate");
  //         frm.refresh_field("payment_of_insurance_copy");

  //         // set sales order items
  //         var i = 0;
  //         frm.clear_table("items");
  //         frm.refresh_field("items");
  //         for (i = 0; i < data.items.length; i++) {
  //           var row = frm.add_child("items");
  //           row.item_code = data.items[i].item_code;
  //           row.item_name = data.items[i].item_name;
  //           row.description = data.items[i].description;
  //           row.uom = data.items[i].uom;
  //           row.qty = data.items[i].current_qty;
  //           row.rate = data.items[i].price;
  //           row.amount = data.items[i].amount;
  //         }
  //         frm.refresh_field("items");
  //       } else {
  //         frappe.throw("Comparison Data Error !");
  //       }
  //     },
  //   });
  // },
  // is_contracting: function (frm) {
  //   if (frm.doc.is_contracting == 0) {
  //     frm.doc.comparison = "";
  //     frm.refresh_field("comparison");
  //     frm.doc.customer = " ";
  //     frm.refresh_field("customer");
  //     frm.clear_table("items");
  //     frm.refresh_field("items");
  //     frm.doc.down_payment_insurance_rate = 0;
  //     frm.doc.payment_of_insurance_copy = 0;
  //     frm.refresh_field("down_payment_insurance_rate");
  //     frm.refresh_field("payment_of_insurance_copy");
  //   }
  // },
  total_cars: function (frm) {
    if (frm.doc.total_cars) {
      frm.set_value("pending_cars", frm.doc.total_cars);
      frm.set_value("not_requested_cars", frm.doc.total_cars);
    }
  },
  // set_contracting(frm) {
  //   frappe.call({
  //     method: "dynamic.contracting.global_data.get_comparison_data",
  //     args: { comparison: frm.doc.comparison },
  //     callback: function (r) {
  //       if (r.message) {
  //         console.log(r.message);
  //         var data = r.message;
  //         // Set customer from comparison
  //         frm.doc.customer = data.customer;
  //         frm.refresh_field("customer");

  //         // set insurance from comparison

  //         frm.doc.down_payment_insurance_rate = data.insurance;
  //         frm.doc.payment_of_insurance_copy = data.d_insurance;
  //         frm.refresh_field("down_payment_insurance_rate");
  //         frm.refresh_field("payment_of_insurance_copy");

  //         // set sales order items
  //         var i = 0;
  //         frm.clear_table("items");
  //         frm.refresh_field("items");
  //         for (i = 0; i < data.items.length; i++) {
  //           var row = frm.add_child("items");
  //           row.item_code = data.items[i].item_code;
  //           row.item_name = data.items[i].item_name;
  //           row.description = data.items[i].description;
  //           row.uom = data.items[i].uom;
  //           row.qty = data.items[i].current_qty;
  //           row.rate = data.items[i].price;
  //           row.amount = data.items[i].amount;
  //         }
  //         frm.refresh_field("items");
  //       } else {
  //         frappe.throw("Comparison Data Error !");
  //       }
  //     },
  //   });
  // },

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

  domian_valid: function (frm) {
    if(cur_frm.doc.docstatus === 1){
      frappe.call({
        method :"dynamic.api.get_active_domains" ,
        async: false,
        callback:function (r){
         if (r.message.includes("Terra")) {
            cur_frm.page.remove_inner_button(__('Update Items'))
            }
        }
    })
    }
 } ,
update_child_items : function(frm,child_docname,child_doctype,cannot_add_row) {
  console.log('okkkk',frm)
	var cannot_add_row = (typeof cannot_add_row === 'undefined') ? true : cannot_add_row;
	var child_docname = (typeof cannot_add_row === 'undefined') ? "items" : child_docname;
	var child_meta = frappe.get_meta(`${frm.doc.doctype} Item`);
  console.log('cannot_add_row ',cannot_add_row,child_docname)

	const get_precision = (fieldname) => child_meta.fields.find(f => f.fieldname == fieldname).precision;

	this.data = [];
	const fields = [{
		fieldtype:'Data',
		fieldname:"docname",
		read_only: 1,
		hidden: 1,
	}, {
		fieldtype:'Link',
		fieldname:"item_code",
		options: 'Item',
		in_list_view: 1,
		read_only: 0,
		disabled: 0,
		label: __('Item Code'),
		get_query: function() {
			let filters;
			if (frm.doc.doctype == 'Sales Order') {
				filters = {"is_sales_item": 1};
			} else if (frm.doc.doctype == 'Purchase Order') {
				if (frm.doc.is_subcontracted == "Yes") {
					filters = {"is_sub_contracted_item": 1};
				} else {
					filters = {"is_purchase_item": 1};
				}
			}
			return {
				query: "erpnext.controllers.queries.item_query",
				filters: filters
			};
		}
	}, {
		fieldtype:'Link',
		fieldname:'uom',
		options: 'UOM',
		read_only: 0,
		label: __('UOM'),
		reqd: 1,
		onchange: function () {
			frappe.call({
				method: "erpnext.stock.get_item_details.get_conversion_factor",
				args: { item_code: this.doc.item_code, uom: this.value },
				callback: r => {
					if(!r.exc) {
						if (this.doc.conversion_factor == r.message.conversion_factor) return;

						const docname = this.doc.docname;
						dialog.fields_dict.trans_items.df.data.some(doc => {
							if (doc.docname == docname) {
								doc.conversion_factor = r.message.conversion_factor;
								dialog.fields_dict.trans_items.grid.refresh();
								return true;
							}
						})
					}
				}
			});
		}
	}, {
		fieldtype:'Float',
		fieldname:"qty",
		default: 0,
		read_only: 0,
		in_list_view: 1,
		label: __('Qty'),
		precision: get_precision("qty")
	}, {
		fieldtype:'Currency',
		fieldname:"rate",
		options: "currency",
		default: 0,
		read_only: 0,
		in_list_view: 1,
		label: __('Rate'),
		precision: get_precision("rate")
	}];

	if (frm.doc.doctype == 'Sales Order' || frm.doc.doctype == 'Purchase Order' ) {
		fields.splice(2, 0, {
			fieldtype: 'Date',
			fieldname: frm.doc.doctype == 'Sales Order' ? "delivery_date" : "schedule_date",
			in_list_view: 1,
			label: frm.doc.doctype == 'Sales Order' ? __("Delivery Date") : __("Reqd by date"),
			reqd: 1
		})
		fields.splice(3, 0, {
			fieldtype: 'Float',
			fieldname: "conversion_factor",
			in_list_view: 1,
			label: __("Conversion Factor"),
			precision: get_precision('conversion_factor')
		})
	}

	const dialog = new frappe.ui.Dialog({
		title: __("Update Items"),
		fields: [
			{
				fieldname: "trans_items",
				fieldtype: "Table",
				label: "Items",
				cannot_add_rows: cannot_add_row,
				in_place_edit: false,
				reqd: 1,
				data: this.data,
				get_data: () => {
					return this.data;
				},
				fields: fields
			},
		],
		primary_action: function() {
			const trans_items = this.get_values()["trans_items"].filter((item) => !!item.item_code);
			frappe.call({
				method: 'erpnext.controllers.accounts_controller.update_child_qty_rate',
				freeze: true,
				args: {
					'parent_doctype': frm.doc.doctype,
					'trans_items': trans_items,
					'parent_doctype_name': frm.doc.name,
					'child_docname': child_docname
				},
				callback: function() {
					frm.reload_doc();
				}
			});
			this.hide();
			refresh_field("items");
		},
		primary_action_label: __('Update')
	});

	frm.doc[child_docname].forEach(d => {
		dialog.fields_dict.trans_items.df.data.push({
			"docname": d.name,
			"name": d.name,
			"item_code": d.item_code,
			"delivery_date": d.delivery_date,
			"schedule_date": d.schedule_date,
			"conversion_factor": d.conversion_factor,
			"qty": d.qty,
			"rate": d.rate,
			"uom": d.uom
		});
		this.data = dialog.fields_dict.trans_items.df.data;
		dialog.fields_dict.trans_items.grid.refresh();
	})
	dialog.show();
},

add_furniture_installation_button(frm) {
  if (frm.doc.docstatus == 1) {
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
        if (r.message && r.message.length) {
          if (r.message.includes("IFI")) {
            frm.add_custom_button(
              __("Installation Furniture Order"),
              function () {
                frm.events.make_furniture_installation_order(frm);
              },
              __("Create")
            );
          }
        }
      },
    });
  }
},

make_furniture_installation_order(frm) {
  frappe.model.open_mapped_doc({
    // installation_request_doc
    method: "dynamic.ifi.api.create_furniture_installation_order",
    frm: frm,

  });
  
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
            // console.log('warehouse -> ',r.message)
            row.warehouse = r.message;
            frm.refresh_fields();
          }
        },
      });
    }
  }
);

// frappe.ui.form.on("Installation Furniture Item", {
// items_add: function (frm, cdt, cdn) {
//   console.log('row_added')
//   // frm.events.set_totals(frm);
// },
// items_remove: function (frm, cdt, cdn) {
//   console.log('row_deleted')
//   // frm.events.set_totals(frm);
// },

// set_totals(frm) {
//   frappe.call({
//     method: "dynamic.ifi.api.set_total",
//     frm: frm,
//     callback: function () {
//       frm.refresh_fields(["items", "total_cars"]);
//     },
//   });
// }
// });

// frappe.ui.form.on("Sales Order Item",{
//     items_remove:function(frm,cdt,cdn){
//       console.log('qty changed standard')
//     },
    
// })

