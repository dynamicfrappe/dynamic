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
  // onload(frm) {
  //   var check_domain = frm.events.domian_valid();
  //   // console.log(check_domain)
  //   if (check_domain && frm.doc.docstatus == 0) {
  //     frm.add_custom_button(
  //       __("view Item Shortage"),
  //       function () {
  //         frappe.call({
  //           method: "dynamic.api.validate_active_domains_invocie",
  //           args: {
  //             doc: frm.doc.name,
  //           },
  //           callback: function (r) {
  //             console.log(r.message);
  //           },
  //         });
  //       },
  //       "view Item Shortage"
  //     );
  //   }
  // },
  onload(frm) {
    var check_domain = frm.events.domian_valid();  
    
    if (check_domain && frm.doc.docstatus == 0) {
        
        frm.add_custom_button(
            __("view Item Shortage"),  
            function () {
                frappe.call({
                    method: "dynamic.api.validate_active_domains_invocie", 
                    args: {
                        doc: frm.doc.name  
                    },
                    callback: function (r) {
                        console.log(r.message);  
                    }
                });
            },
            "view Item Shortage" 
        );
    } else {
      frappe.call({
          method: "dynamic.api.get_active_domains", 
          callback: function(r) {
              if (r.message && r.message.includes("Qaswaa")) {
                  console.log("baio");
                  if (frm.doc.is_return == 1) {
                      frm.fields_dict['sales_team'].grid.toggle_enable('sales_person', false);
                      frm.refresh_field('sales_team');   
                  }
              }
          }
      });
  }
}, 
  


  refresh(frm) {
    frm.events.add_cheque_button(frm);
    frm.events.set_query(frm)
    frm.events.upload_data_file(frm)
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
  upload_data_file:function(frm){
    frm.fields_dict["items"].grid.add_custom_button(
      __("Upload Xlxs Data"),
      function() {
          let d = new frappe.ui.Dialog({
              title: "Enter details",
              fields: [
                {
                  label: "Excel File",
                  fieldname: "first_name",
                  fieldtype: "Attach",
                },
              ],
              primary_action_label: "Submit",
              primary_action(values) {
                console.log(`values===>${JSON.stringify(values)}`);
                var f = values.first_name;
                frappe.call({
                  method:"dynamic.api.get_data_from_template_file",
                  args: {
                    file_url: values.first_name
                    // file: values.first_name,
                    // colms:['item_code','qty',]
                  },
                  callback: function(r) {
                    if (r.message) {
                      console.log(r.message)
                      frm.clear_table("items");
                      frm.refresh_fields("items");
                      r.message.forEach(object => {
                        var row = frm.add_child("items");
                        Object.entries(object).forEach(([key, value]) => {
                          //  console.log(`${key}: ${value}`);
                          row[key] = value;
                        });
                       });
                      frm.refresh_fields("items");
                    }
                  },
                });
                d.hide();
              },
            });
            d.show();
      }).addClass("btn-success");
      frm.fields_dict["items"].grid.grid_buttons
      .find(".btn-custom")
      .removeClass("btn-default")
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

add_item_discount_rate: function(frm) {
  var item_discount_rate = frm.doc.item_discount_rate;
        frm.doc.items.forEach(function(item) {
            frappe.model.set_value(item.doctype, item.name, 'discount_percentage', item_discount_rate);
        });
        frm.refresh_field('items');
},


  item_discount_rate: function(frm) {
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function(r) {
        if (r.message && r.message.length) {
          if (r.message.includes("Qaswaa")) {
            console.log("Catech !!")
            // frm.events.add_item_discount_rate(frm);
          }
        }
      }
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


// frappe.ui.form.on("Sales Team", {
//   sales_person:function(frm,cdt,cdn){
//     let row = locals[cdt][cdn]
//     if (row.sales_person && frm.doc.docstatus==1){
//       frm.call({
//         method:"dynamic.api.validate_active_domains",
//         args:{
//           doc:frm.doc
//         },
//         callback:function(r){
//           // console.log('return --------->')
//         }
//       })
//     }
//   }

// })





frappe.ui.form.on("Sales Invoice Item", {
//   items_add: function(frm,cdt,cdn) {
//     console.log("baio");
//     frappe.call({
//         method: "dynamic.api.get_active_domains",
//         callback: function(r) {
//             if (r.message && r.message.length && r.message.includes("Qaswaa")) {
//               frm.events.add_item_discount_rate(frm);
//             }
//         }
//     });
// },
  item_code:function(frm,cdt,cdn){
    let row = locals[cdt][cdn]
    if(row.item_code){
     
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length && r.message.includes("Qaswaa")) {
                console.log("bgg");
                var item_discount_rate = frm.doc.item_discount_rate;
                console.log(item_discount_rate);
                if (item_discount_rate ){
                row.discount_percentage = item_discount_rate
                // frm.set_value("items","discount_percentage",item_discount_rate)
               
                frm.refresh_fields("items");
         }
            }
        }
    }); 
      frm.refresh_fields('items');
    }
  },
  qty:function(frm,cdt,cdn){
    let row = locals[cdt][cdn]
    row.total = row.base_price_list_rate * row.qty
    frm.refresh_fields('items')
  },

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
         
          }
        }
      }
    })

    
  },
  

  
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