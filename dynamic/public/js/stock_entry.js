
frappe.ui.form.on("Stock Entry", {


    setup :function(frm){
      frm.events.set_field_property(frm)

    //   frappe.call({
    //       "method" : "dynamic.contracting.doctype.stock_functions.fetch_contracting_data" ,
    //       callback :function(r){
    //         console.log(r)
    //         if (r.message){

    //         }
    //       }
    //   })
       
    },
    // transit:function(frm){
    //   if(frm.doc.stock_entry_type == 'Material Transfer'){
    //     frappe.call({
    //       method: "dynamic.api.get_active_domains",
    //       callback: function (r) {
    //           if (r.message && r.message.length) {
    //               if (r.message.includes("WEH")) {
    //                 frm.set_df_property("add_to_transit", "read_only", 1)
    //                 if(frm.doc.transit){
    //                   frm.set_value("add_to_transit", 1)
    //                 }
    //                 else{
    //                   frm.set_value("add_to_transit", 0)
    //                 }
                   
                    
    //               }
    //               frm.refresh_field("add_to_transit")
    //           }
    //       }
    //   })
    //   }
    // },
    set_field_property(frm){
      if(frm.doc.stock_entry_type == 'Material Transfer'){
        frappe.call({
          method: "dynamic.api.get_active_domains",
          callback: function (r) {
              if (r.message && r.message.length) {
                  if (r.message.includes("WEH")) {
                    frm.set_df_property("add_to_transit", "reqd", 1)
                    // frm.set_value('add_to_transit',1)
                    frm.refresh_field("add_to_transit")
                  }
              }
          }
      })
      }
    },
    trea_setup(frm){
      frappe.call({
        method:"dynamic.api.validate_terra_domain",
        callback:function(r) {
          if (r.message){
            frm.events.terra_stock_etnrty(frm)
          }
        }
       })
  
    },
    terra_stock_etnrty(frm){
      if (frm.doc.add_to_transit === 0){
      
          frm.remove_custom_button(__('End Transit')) 
        
        }
      if (frm.doc.__islocal && frm.doc.outgoing_stock_entry) {

        frappe.call({
          method: 'frappe.client.get_value',
          "args":{
            "doctype": 'Stock Entry',
            "fieldname": "ds_warehouse",
            "filters": {
              'name': frm.doc.outgoing_stock_entry,
            
            },
          },
          callback: function (data) {
             frm.set_value("to_warehouse" ,  data.message.ds_warehouse )
             frm.set_df_property("to_warehouse", 'read_only', 1);
             frm.refresh_field("to_warehouse")
          }

        })
       
        

      }
      
    },
    onload:function(frm) {
    //  add tarra customization 
    
     frm.events.trea_setup(frm)
     
    },
    refresh:function(frm){
      frm.events.trea_setup(frm)
      frm.events.set_property(frm)
      // frm.events.set_property_domain(frm)
      frm.events.set_field_property(frm)
      frm.events.transit_btn(frm)
    },
    stock_entry_type : function (frm){
      frm.events.filter_stock_entry_transfer(frm)
      // frm.events.set_property_domain(frm)
      frm.events.set_field_property(frm)
    },
    filter_stock_entry_transfer(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("Lormed")) {
                  if (frm.doc.stock_entry_type == "Repack"){
                    frm.set_query("stock_entry_transfer_type", () => {
                    return { filters: {"stock_entry_type": "Material Transfer" }
                    }});
                  }
                }
            }
        }
    })

    },
    add_to_transit : function (frm) {
      frm.events.set_property(frm)
    },
    set_property(frm){
      var ds_warehouse_reqrd = (frm.doc.add_to_transit == 1) ? 1:0
      frm.set_df_property("ds_warehouse", "reqd", ds_warehouse_reqrd )
      frm.refresh_field("ds_warehouse")
      if(frm.doc.repack){
        frm.set_df_property("from_warehouse", "read_only", 1);
        frm.set_df_property("to_warehouse", "read_only", 1);
      }
    },
    transit_btn:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("WEH")) {
                  if (frm.doc.docstatus === 1) {
                    if (frm.doc.add_to_transit && frm.doc.purpose=='Material Transfer' && frm.doc.per_transferred < 100) {
                      frm.remove_custom_button('End Transit')
                      frm.add_custom_button('End Transit', function() {
                        frappe.model.open_mapped_doc({
                          method: "dynamic.weh.api.make_stock_in_entry",
                          frm: frm
                        })
                      });
                    }
                  }
                 frm.cscript['toggle_related_fields'] = _toggle_related_fields_weh
                
                }
            }
        }
    })
      
    },
    
    set_property_domain:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("Stock Transfer")) {
                  if (frm.doc.stock_entry_type == "Material Transfer"){
                  }
                }
            }
        }
    })
      
    },
    
    comparison : function (frm) {
        if(frm.doc.against_comparison){
          frappe.call({
            "method" : "contracting.contracting.doctype.stock_functions.stock_entry_setup" ,
            args:{
              "comparison" : frm.doc.comparison,
            },
            callback :function(r){
              if (r.message){

                frm.set_query("comparison_item",function () {
                  return {
                    filters: [
                      ["item_code", "in", r.message],
                    ],
                  };
                });
                frm.refresh_field("comparison_item")
                frm.set_query("comparison_item","items",function () {
                  return {
                    filters: [
                      ["item_code", "in", r.message],
                    ],
                  };
                });
                frm.refresh_field("items")
              }
            } 
         
          })
      }
    },

    
    cost_center:function(frm){
      if(frm.doc.cost_center){
        frappe.call({
          method: "dynamic.api.get_active_domains",
          callback: function (r) {
              if (r.message && r.message.length) {
                  if (r.message.includes("Maser2000")) {
                    $.each(frm.doc.items || [], function(i, d) {
                      d.cost_center = frm.doc.cost_center;
                    });
                    refresh_field("items");
                  }
              }
          }
      })
      }
    },
    get_target_warehouse_details: function(frm, cdt, cdn) {
      var child = locals[cdt][cdn];
      if (child.item_code){
        if(!child.bom_no && child.t_warehouse) {
          frappe.call({
            method: "erpnext.accounts.doctype.pos_invoice.pos_invoice.get_stock_availability", //"erpnext.stock.doctype.stock_entry.stock_entry.get_warehouse_details",
            args:{
              'item_code': child.item_code,
              'warehouse': cstr(child.t_warehouse),
            },
            // args: {
            //   "args": {
            //     'item_code': child.item_code,
            //     'warehouse': cstr(child.t_warehouse),
            //     'transfer_qty': child.transfer_qty,
            //     'serial_no': child.serial_no,
            //     'qty': child.s_warehouse ? -1* child.transfer_qty : child.transfer_qty,
            //     'posting_date': frm.doc.posting_date,
            //     'posting_time': frm.doc.posting_time,
            //     'company': frm.doc.company,
            //     'voucher_type': frm.doc.doctype,
            //     'voucher_no': child.name,
            //     'allow_zero_valuation': 1
            //   }
            // },
            callback: function(r) {
              if (!r.exc){
                // console.log(r.message)
                frappe.model.set_value(cdt, cdn, 'qty_target', (r.message[0] || 0.0));
                // ["actual_qty", "basic_rate"].forEach((field) => {
                //   frappe.model.set_value(cdt, cdn, field, (r.message[field] || 0.0));
                // });
                // frm.events.calculate_basic_amount(frm, child);
              }
            }
          });
        }
      }

    },


})


frappe.ui.form.on('Stock Entry Detail', {
  t_warehouse: function(frm, cdt, cdn) {
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
          if (r.message && r.message.length) {
              if (r.message.includes("WEH")) {
                frm.events.get_target_warehouse_details(frm, cdt, cdn);
                refresh_field("items");
              }
          }
      }
  })
  },
  
})




function _toggle_related_fields_weh(){
  cur_frm.toggle_enable("from_warehouse", cur_frm.doc.purpose!='Material Receipt');
  cur_frm.toggle_enable("from_warehouse", !cur_frm.doc.outgoing_stock_entry);
  cur_frm.toggle_enable("to_warehouse", cur_frm.doc.purpose!='Material Issue');

  cur_frm.fields_dict["items"].grid.set_column_disp("retain_sample", cur_frm.doc.purpose=='Material Receipt');
  cur_frm.fields_dict["items"].grid.set_column_disp("sample_quantity", cur_frm.doc.purpose=='Material Receipt');

  cur_frm.cscript.toggle_enable_bom();

  if (cur_frm.doc.purpose == 'Send to Subcontractor') {
    cur_frm.doc.customer = cur_frm.doc.customer_name = cur_frm.doc.customer_address =
      cur_frm.doc.delivery_note_no = cur_frm.doc.sales_invoice_no = null;
  } else {
    cur_frm.doc.customer = cur_frm.doc.customer_name = cur_frm.doc.customer_address =
      cur_frm.doc.delivery_note_no = cur_frm.doc.sales_invoice_no = cur_frm.doc.supplier =
      cur_frm.doc.supplier_name = cur_frm.doc.supplier_address = cur_frm.doc.purchase_receipt_no =
      cur_frm.doc.address_display = null;
  }
  if(cur_frm.doc.purpose == "Material Receipt") {
    cur_frm.set_value("from_bom", 0);
  }

  // Addition costs based on purpose
  cur_frm.toggle_display(["additional_costs", "total_additional_costs", "additional_costs_section"],
    cur_frm.doc.purpose!='Material Issue');

  cur_frm.fields_dict["items"].grid.set_column_disp("additional_cost", cur_frm.doc.purpose!='Material Issue');
}
