frappe.ui.form.on("Sales Invoice", {
  setup(frm) {
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
        if (r.message && r.message.length) {
          if (r.message.includes("Cheques")) {
              frm.custom_make_buttons["Cheque"] = "Cheque";
          }
      }}
  })
  },
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
    frm.events.add_cheque_button(frm);
    frm.events.set_query(frm)
    // const myTimeout = setTimeout(get_customer_query, 1300);


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
  brand:function(frm){
    frm.fields_dict.items.grid.get_field("item_code").get_query = function () {
      return {
        filters: [
          ["brand", "=", cur_frm.doc.brand],
        ],
      };
    };
  },
  set_query:function(frm){
    frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
          if (r.message && r.message.length) {
            if (r.message.includes("Real State")) {
              frm.set_query('item_code', 'items', function(doc, cdt, cdn) {
                return {
                  filters:{"reserved":0}
                };
              });
            }
        }}
    })
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
  cost_center:function(frm){
    if(frm.doc.cost_center){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
          if (r.message && r.message.length) {
            if (r.message.includes("Cost Center")) {
                $.each(frm.doc["items"] || [], function(i, item) {
                  item.cost_center = flt(frm.doc.cost_center);
                });
                frm.refresh_field("items");
              }
            }
          }
      })
  }
    
  },

});

function get_customer_query(){
  frappe.call({
    method: "dynamic.api.get_active_domains",
    callback: function (r) {
      if (r.message && r.message.length) {
        if (r.message.includes("Master Deals")) {
          cur_frm.set_query('customer',(doc)=>{
            return {
              query: 'dynamic.master_deals.master_deals_api.customer_query_custom',
              filters:{"docname":cur_frm.doc.name}
            }
            
          })
        }
      }
    },
  });
  
}


frappe.ui.form.on("Sales Team", {
  sales_person:function(frm,cdt,cdn){
    let row = locals[cdt][cdn]
    if (row.sales_person && frm.doc.docstatus==1){
      frm.call({
        method:"dynamic.api.validate_active_domains",
        args:{
          doc:frm.doc
        },
        callback:function(r){
          // console.log('return --------->')
        }
      })
    }
  }

})


frappe.ui.form.on("Sales Invoice Item", {
  item_code:function(frm,cdt,cdn){
    let row = locals[cdt][cdn]
    if(row.item_code){
      frappe.call({
				'method': 'frappe.client.get_value',
				'args': {
					'doctype': 'Item Price',
					'filters': {
						'item_code': row.item_code,
            "selling":1
					},
				   'fieldname':'price_list_rate'
				},
				'callback': function(res){
					row.total =  res.message.price_list_rate;
				}
			});
      
      frm.refresh_fields('items')
    }
  },
  qty:function(frm,cdt,cdn){
    let row = locals[cdt][cdn]
    row.total = row.base_price_list_rate * row.qty
    frm.refresh_fields('items')
  }
})



const extend_sales_invoice = erpnext.accounts.SalesInvoiceController.extend({
  refresh: function(doc, dt, dn) {
		const me = this;
		this._super(doc,dt,dn);
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
        if (r.message && r.message.length) {
          // console.log('domains ',r.message)
          if(r.message.includes("Qaswaa")){
            // sales invoice
            if (doc.docstatus == 1 && doc.outstanding_amount!=0
              && !(cint(doc.is_return) && doc.return_against)) {
                cur_frm.cscript['make_payment_entry'] = create_payment_sales_person //new
                // cur_frm.page.remove_inner_button('Payment', 'Create')
            }
            // add button Purchase Invoice
          // if (!this.frm.is_new() && this.frm.doc.docstatus === 0) {
          //   this.frm.add_custom_button(__("Purchase Invoice"), () => {
          //     me.make_purchase_invoice();
          //   }, __("Create"));
          // }
             
          }
        }
      }
    })

    
  },

  // make_purchase_invoice() {
	// 	let data = [];
	// 	const fields = [
	// 		{
	// 			label: "Items",
	// 			fieldtype: "Table",
	// 			fieldname: "items",
	// 			cannot_add_rows: true,
	// 			in_place_edit: true,
	// 			data: data,
	// 			get_data: () => {
	// 				return data;
	// 			},
	// 			fields: [
	// 				{
	// 					fieldtype: "Data",
	// 					fieldname: "docname",
	// 					hidden: true
	// 				},
	// 				{
	// 					fieldtype: "Read Only",
	// 					fieldname: "item_code",
	// 					label: __("Item Code"),
	// 					in_list_view: true
	// 				},
	// 				{
	// 					fieldtype: "Read Only",
	// 					fieldname: "item_name",
	// 					label: __("Item Name"),
	// 					in_list_view: true
	// 				},
	// 				{
	// 					fieldtype: "Float",
	// 					fieldname: "qty",
	// 					label: __("Accepted Quantity"),
	// 					in_list_view: true,
	// 					read_only: true
	// 				},
	// 				{
	// 					fieldtype: "Float",
	// 					fieldname: "sample_size",
	// 					label: __("Sample Size"),
	// 					reqd: true,
	// 					in_list_view: true
	// 				},
	// 				{
	// 					fieldtype: "Data",
	// 					fieldname: "description",
	// 					label: __("Description"),
	// 					hidden: true
	// 				},
	// 				{
	// 					fieldtype: "Data",
	// 					fieldname: "serial_no",
	// 					label: __("Serial No"),
	// 					hidden: true
	// 				},
	// 				{
	// 					fieldtype: "Data",
	// 					fieldname: "batch_no",
	// 					label: __("Batch No"),
	// 					hidden: true
	// 				}
	// 			]
	// 		}
	// 	];

	// 	const me = this;
	// 	const dialog = new frappe.ui.Dialog({
	// 		title: __("Select Items for Quality Inspection"),
	// 		fields: fields,
	// 		primary_action: function () {
	// 			const data = dialog.get_values();
	// 			frappe.call({
	// 				method: "erpnext.controllers.stock_controller.make_quality_inspections",
	// 				args: {
	// 					doctype: me.frm.doc.doctype,
	// 					docname: me.frm.doc.name,
	// 					items: data.items
	// 				},
	// 				freeze: true,
	// 				callback: function (r) {
	// 					if (r.message.length > 0) {
	// 						if (r.message.length === 1) {
	// 							frappe.set_route("Form", "Quality Inspection", r.message[0]);
	// 						} else {
	// 							frappe.route_options = {
	// 								"reference_type": me.frm.doc.doctype,
	// 								"reference_name": me.frm.doc.name
	// 							};
	// 							frappe.set_route("List", "Quality Inspection");
	// 						}
	// 					}
	// 					dialog.hide();
	// 				}
	// 			});
	// 		},
	// 		primary_action_label: __("Create")
	// 	});

	// 	this.frm.doc.items.forEach(item => {
	// 		if (!item.quality_inspection) {
	// 			let dialog_items = dialog.fields_dict.items;
	// 			dialog_items.df.data.push({
	// 				"docname": item.name,
	// 				"item_code": item.item_code,
	// 				"item_name": item.item_name,
	// 				"qty": item.qty,
	// 				"description": item.description,
	// 				"serial_no": item.serial_no,
	// 				"batch_no": item.batch_no,
	// 				"sample_size": item.sample_quantity
	// 			});
	// 			dialog_items.grid.refresh();
	// 		}
	// 	});

	// 	data = dialog.fields_dict.items.df.data;
	// 	if (!data.length) {
	// 		frappe.msgprint(__("All items in this document already have a linked Quality Inspection."));
	// 	} else {
	// 		dialog.show();
	// 	}
	// },
  
})

$.extend(
	cur_frm.cscript,
	new extend_sales_invoice({frm: cur_frm}),
);


var create_payment_sales_person = function() {
  return frappe.call({
    method: "dynamic.qaswaa.utils.qaswaa_api.get_payment_entry",
    args: {
      'dt': cur_frm.doc.doctype,
      'dn': cur_frm.doc.name
    },
    callback: function(r) {
      var doc = frappe.model.sync(r.message);
      frappe.set_route('Form', doc[0].doctype, doc[0].name);
    }
  });
  // frappe.model.open_mapped_doc({
  //   method: "dynamic.qaswaa.utils.qaswaa_api.get_payment_entry",
  //   frm: cur_frm
  // })
}