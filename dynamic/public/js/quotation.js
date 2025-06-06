frappe.ui.form.on("Quotation",{
    // onload:function(frm) {
    //     frm.events.refresh(frm)
    // },
    refresh:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
          if (r.message.includes("Real State")) {
              if(frm.doc.docstatus == 1){
                cur_frm.add_custom_button(__('Payment Entry'),
                cur_frm.cscript['Make Payment Entry'], __('Create'));
              }
          }
          if (r.message && r.message.length) {
            if (r.message.includes("Pre Quotation")) {
              frm.events.upload_data_file(frm)
              frm.fields_dict["items"].grid.add_custom_button(
                __("Export Excel"),
                function() {
                // console.log("frm.items");
                frappe.call({
                  method: "dynamic.api.export_data_to_csv_file",
                  args: {
                  items: frm.doc.items,
                  },
                  callback: function(r) {
                  if (r.message){
                    let file = r.message.file 
                    let file_url = r.message.file_url 
                    file_url = file_url.replace(/#/g, '%23');
                    window.open(file_url);
                  }
                  },
                });
            
                }
              );
            }
          }
        }
    })

      
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Terra")) {
                    cur_frm.cscript['Make Sales Order'] = create_terra_sales_order
                    if (frm.doc.docstatus == 1) {
                        if (frm.doc.quotation_to == "Lead"){
                            frappe.db.get_value("Customer", {"lead_name": frm.doc.party_name}, "name", (r) => {
                                if(!r.name){
                                cur_frm.add_custom_button(__('Customer'),function(){
                                    frappe.call({
                                        method:"dynamic.terra.doctype.quotation.quotation.make_customer",
                                        args:{
                                            source_name:frm.doc.name,
                                        },
                                        callback:function(r){
                                            frm.refresh()
                                        }
        
                                    })
                                }
                                , __('Create'));	 
                                }						
                            });
                            }
                        cur_frm.add_custom_button(__('Payment Entry'),
                                cur_frm.cscript['Make Payment Entry'], __('Create'));
                       
                    }
                }
                if (r.message.includes("IFI")) {
                    if(frm.doc.docstatus == 1){
                        frm.add_custom_button("Potential",()=>{
                            frappe.confirm('Are you sure you want to Potential quotation',
                                () => {
                                    frappe.call({
                                        method:"dynamic.ifi.api.set_potential_status",
                                        args:{
                                            frm_name:frm.doc.name,
                                        },
                                        callback:function(r){
                                             frm.refresh()
                                        }
            
                                    })
                                }, () => {
                                    // action to perform if No is selected
                                })
    
                        })
                    }
                    
                    
               
                };
                if (r.message.includes("Qaswaa")){
                    cur_frm.cscript['Make Sales Order'] = create_qaswaa_sales_order
                };
                   
            }
        }
    })
    frm.events.set_query(frm)

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
    reject_quotation(frm){
        frm.call({
            method:"dynamic.ifi.doctype.installations_furniture.installations_furniture.reqject_quotation",
            args:{
                source_name:frm.doc.name, 
            },
            callback:function(r){
                frm.reload_doc()
            }

        })
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
    

    get_advancess:function(frm){
        if(!frm.is_return) {
                frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Dynamic Accounts")) {
                  console.log("Hi");
                  return frappe.call({
                    method: "dynamic.ifi.api.get_advance_entries_quotation",//get_advanced_so_ifi
                    args:{
                        doc_name: frm.doc.name,
                    },
                    callback: function(r, rt) {
                      console.log(r.message);
                      frm.clear_table("advancess");
                      let total = 0 ;
                      r.message.forEach(row => {
                        console.log("Hi");
                        console.log(row);
                        let child = frm.add_child("advancess");
                        child.reference_type = row.reference_type,
                        child.reference_name = row.reference_name,
                        child.reference_row = row.reference_row,
                        child.remarks = row.remarks,
                        child.advance_amount = flt(row.amount),
                        child.allocated_amount = row.allocated_amount,
                        child.ref_exchange_rate = flt(row.exchange_rate)
                        total += parseFloat(row.amount);
                      });
                      refresh_field("advancess");
                      frm.set_value("advance_paid" , total);
                      frm.refresh_field("advance_paid");
                      let base_grand_total = parseFloat(frm.doc.grand_total);
                      frm.set_value("outstanding_amount" , base_grand_total - total);
                      frm.refresh_field("base_grand_total");
                    }
                  })
                }
            }}
        })
            }
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
                  console.log("ass")
                  frm.events.add_item_discount_rate(frm);
                }
              }
            }
          });
        },  
})



const QuotationController_Extend = erpnext.selling.QuotationController.extend({
  
	refresh: function(doc, dt, dn) {
		this._super(doc);
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("IFI")) {
                    cur_frm.page.remove_inner_button('Subscription','Create')
                    cur_frm.cscript['Make Sales Order'] = create_ifi_sales_order
                    // cur_frm.cscript['Make Payment Entry'] = create_ifi_payment_entry
                    if(doc.docstatus == 1 && doc.status!=='Lost') {
                        if(!doc.valid_till || frappe.datetime.get_diff(doc.valid_till, frappe.datetime.get_today()) >= 0) {
                            cur_frm.page.remove_inner_button('Sales Order','Create')
                            cur_frm.add_custom_button(__('Sales Order'),
                                cur_frm.cscript['Make Sales Order'], __('Create'));
                        }
                    }
                }
              }
            }
            })
	},
})

$.extend(
	cur_frm.cscript,
	new QuotationController_Extend({frm: cur_frm}),
);

var create_ifi_sales_order = function() {

    frappe.model.open_mapped_doc({
		method: "dynamic.ifi.api.make_sales_order",
		frm: cur_frm
	})
}

var create_terra_sales_order = function() {

    frappe.model.open_mapped_doc({
		method: "dynamic.terra.doctype.quotation.quotation.make_sales_order",
		frm: cur_frm
	})
}


var create_qaswaa_sales_order = function() {

    frappe.model.open_mapped_doc({
		method: "dynamic.qaswaa.controllers.qaswaa_api.create_qaswaa_sales_order",
		frm: cur_frm
	})
}


// var create_ifi_payment_entry = function() {
//     frappe.model.open_mapped_doc({
//         method:
//         "dynamic.terra.api.get_payment_entry_quotation",
//         frm: cur_frm,
//       });
// }

frappe.ui.form.on("Quotation Item", {
//     item_code: function(frm, cdt, cdn) {
//     var child = locals[cdt][cdn];
//     var parent_discount_rate = frm.doc.item_discount_rate;

//     frappe.call({
//         method: "dynamic.api.get_active_domains",
//         callback: function (r) {
//             if (r.message && r.message.length && r.message.includes("Qaswaa")) {
//                 console.log("bgg");
//                 console.log(parent_discount_rate);
//                 frm.set_value("items", "discount_percentage", parent_discount_rate);
//                 frm.refresh_fields("items");
//             }
//         }
//     });
// }
    // item_code:function(frm,cdt,cdn){
    //   let row = locals[cdt][cdn]
    //   if(row.item_code){
    //     frappe.call({
    //               'method': 'frappe.client.get_value',
    //               'args': {
    //                   'doctype': 'Item Price',
    //                   'filters': {
    //                       'item_code': row.item_code,
    //                       "selling":1
    //                   },
    //                  'fieldname':'price_list_rate'
    //               },
    //               'callback': function(res){
    //                 console.log(`item prdice ---> ${res.message.price_list_rate}`)
    //                   row.grand_total =  res.message.price_list_rate;
    //               }
    //           });
        
    //     frm.refresh_fields('items')
    //   }
    // },
    // qty:function(frm,cdt,cdn){
    //   let row = locals[cdt][cdn]
    //   row.grand_total = row.base_price_list_rate * row.qty
    //   frm.refresh_fields('items')
    // }
  })

cur_frm.cscript['Make Payment Entry'] = function() {
    frappe.model.open_mapped_doc({
        method:
        "dynamic.terra.api.get_payment_entry_quotation",
        frm: cur_frm,
      });
}

frappe.ui.form.on('Quotation', {
  onload: function(frm) {
      frm.fields_dict['payment_schedule'].grid.get_field('payment_term').get_query = function(doc, cdt, cdn) {
          return {
              filters: {
                  is_usable: 1
              }
          };
      };
  }
});
