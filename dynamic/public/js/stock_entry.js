frappe.ui.form.on("Stock Entry", {  
  customer_id:function(frm){
    let stock_entry_type = frm.doc.stock_entry_type;
    console.log(stock_entry_type);
      if (stock_entry_type){
        let matrial_type = get_data("Stock Entry Type" , stock_entry_type);
        if (matrial_type.matrial_type === "Received Simples"){
          frm.set_df_property('old_stock_entry', 'hidden', 0);
          frm.set_query('old_stock_entry', () => {
            return {
                filters: {
                    customer_id: frm.doc.customer_id , 
                    stock_entry_type: get_ops()
                }
            }
          })
        }
      }
    },
     
    old_stock_entry:function(frm){
      let old_stock_entry = frm.doc.old_stock_entry ;
        if(old_stock_entry){
            let doc = get_data ("Stock Entry" , old_stock_entry);
            let items = doc.items ;
            frm.clear_table("items");
            for (let item of items){
              frm.add_child('items', {
                "actual_qty": item.actual_qty,
                "additional_cost": item.additional_cost,
                "allow_zero_valuation_rate": item.allow_zero_valuation_rate , 
                "amount": item.amount,
                "barcode": item.barcode , 
                "basic_amount": item.basic_amount , 
                "basic_rate": item.basic_rate , 
                "batch_no": item.batch_no,
                "bom_no": item.bom_no, 
                "conversion_factor": item.conversion_factor,
                "cost_center": item.cost_center , 
                "description": item.description , 
                "image" : item.image , 
                "item_code" : item.item_code , 
                "item_group": item.item_group , 
                "item_name": item.item_name , 
                "uom": item.uom , 
                "valuation_rate": item.valuation_rate,
                "t_warehouse":item.s_warehouse,
                "qty":item.qty
  
              });
            }
        frm.refresh_field('items');
      }
    }
  })

 
  function get_ops(){
    var temp ;
    frappe.call({
      async:false,
      method: 'frappe.client.get',
      args: {
          doctype: "Stock Entry Type",
          filters:{
            "matrial_type" : "Dispensing Simples"
          },
      },
      callback: (r) => {
        temp = r.message.name;
      },
    })
    return temp ;
  }
  
  function get_data(doctype , name ){
    var temp ;
    frappe.call({
      async:false,
      method: 'frappe.client.get',
      args: {
          doctype: doctype,
          name:name,
      },
      callback: (r) => {
        temp = r.message;
      },
    })
    return temp ;
  }


frappe.ui.form.on("Stock Entry", {


    setup :function(frm){
      frm.events.set_field_property(frm)

    //   frappe.call({
    //       "method" : "dynamic.contracting.doctype.stock_functions.fetch_contracting_data" ,
    //       callback :function(r){
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
    on_submit:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("WEH")) {
                 frappe.set_route('List', "Stock Entry", 'List')
                }
            }
        }
    })
    },
    set_posting_time:function(frm){
      frm.events.set_field_property(frm)
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("WEH")) {
                   if (frm.is_dirty) {
                    frm.enable_save()
                   }
                }
            }
        }
    })
      
    },
    setup_source_warehouse(frm){
      frappe.call({
        "method" : "dynamic.weh.controllers.get_defaulte_source_warehouse",
        callback:function(r) {
          if (r.message) {
          
            if(frm.is_new()){
              frm.set_value("from_warehouse" , r.message[0]) 
           frm.refresh_field("from_warehouse")
            } 
            if(!frm.is_new()){
              if (! r.message.includes(frm.doc.to_warehouse) ){
                console.log("Disable Save")
                frm.disable_save()
              }
            }
            
           
           
           
          // frm.set_query("from_warehouse", function(){
          //   console.log(r.message)
          //   return {
          //     "filters": [
          //         ["Warehouse", "name", "in", r.message],
              
          //     ]
          // }
          // })

         if (r.message.length == 1){
          frm.set_df_property("from_warehouse", "read_only", 1);
          frm.refresh_field("from_warehouse")
         }
        }
        }
      })


    },
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
      
     
      // frm.custom_transaction_controller = new erpnext.CustomTransactionController(frm);
      frm.events.trea_setup(frm)
      frm.events.set_property(frm)
      // frm.events.set_property_domain(frm)
      frm.events.set_field_property(frm)
      frm.events.transit_btn(frm)
      frm.events.read_only_fields(frm)
    },
    read_only_fields:function(frm){
      frm.events.setup_source_warehouse(frm)
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) { 
          if (frm.doc.owner != frappe.session.user) {
            console.log("not Owner")
            frm.set_read_only()
          }
      //     if (r.message && r.message.length) {
      //       if (r.message.includes("WEH")) {
      //         frm.events.setup_source_warehouse(frm)
      //         // frappe.call({
      //         //   method:"dynamic.weh.api.get_roles_hidden_field",
      //         //   args:{
      //         //     "field_hide":"stock_entry_read_only",
      //         //     "field_empty":"empty_source_warehouse_role",
      //         //   },
      //         //   callback:function(r) {
      //         //     frm.set_df_property("from_warehouse", "read_only", r.message.hide);
      //         //     if(r.message.empty){
      //         //       frm.set_value("from_warehouse","")
      //         //     }
      //         //     frm.refresh_fields("from_warehouse")
      //         //   }
      //         //  })
               
      //   }
      // }
      }
    })
      
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
    item_code_update:function(frm ,cdt , cdn){
      // this function work with domain master Deals only 
      var local = locals[cdt][cdn]
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("Master Deals")) {
                    console.log("Master Deals In Active Domains ")
                    // call api to get current available qty 
                    if (frm.doc.from_warehouse || local.s_warehouse ) {
                    
                      var args = {"item" : local.item_code ,
                      "s_warehouse" :local.s_warehouse || frm.doc.from_warehouse ,
                      "purpose" :frm.doc.stock_entry_type ,
                     }
                      if (!frm.__islocal) {
                        console.log("Old Document !")
                        args = {"item" : local.item_code ,
                                "s_warehouse" :local.s_warehouse || frm.doc.from_warehouse ,
                                "purpose" :frm.doc.stock_entry_type ,
                                "doc" : frm.doc.name
                                }
                      }
                      frappe.call({
                        method :"dynamic.master_deals.master_deals_api.get_current_item_available_qty" ,
                        "args" :args ,
                        callback:function(r){
                          console.log(r)
                          if (r.message){
                            local.available_qty = r.message
                            frm.refresh_field("items")
                          }
                          else {
                            local.available_qty =0
                            frm.refresh_field("items")
                          }
                        }
                      })
                    }
                   
  
  
  
  
                }
            }
        }
    })
    }


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
  item_code:function(frm ,cdt , cdn){
    frm.events.item_code_update(frm ,cdt , cdn)
  },
  s_warehouse:function(frm ,cdt , cdn){
    frm.events.item_code_update(frm ,cdt , cdn)
  },
  
})




function _toggle_related_fields_weh(){
  // cur_frm.toggle_enable("from_warehouse", cur_frm.doc.purpose!='Material Receipt');
  // cur_frm.toggle_enable("from_warehouse", !cur_frm.doc.outgoing_stock_entry);
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

//******* */
const override_scan_code = erpnext.stock.StockEntry.extend({
  scan_barcode: function() {
    me = this
		let transaction_controller= new erpnext.TransactionController({frm:this.frm});
    // transaction_controller.scan_barcode = this.override_scan_barcode()
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
          if (r.message && r.message.length) {
              if (r.message.includes("Master Deals")) {
                transaction_controller.scan_barcode = me.override_scan_barcode()
              }
              else{
                transaction_controller.scan_barcode()
              }
          }
      }
  })
		
		
	},
	override_scan_barcode: function() {
		let me = this;

		if(this.frm.doc.scan_barcode) {
			frappe.call({
				method: "erpnext.selling.page.point_of_sale.point_of_sale.search_for_serial_or_batch_or_barcode_number",
				args: {
					search_value: this.frm.doc.scan_barcode
				}
			}).then(r => {
				const data = r && r.message;
				if (!data || Object.keys(data).length === 0) {
					frappe.show_alert({
						message: __('Cannot find Item with this Barcode'),
						indicator: 'red'
					});
					return;
				}

				me.modify_table_after_scan(data);
			});
		}
		return false;
	},
	modify_table_after_scan(data) {
		let scan_barcode_field = this.frm.fields_dict["scan_barcode"];
		let cur_grid = this.frm.fields_dict.items.grid;
		let row_to_modify = null;
    let new_row = 0
		// Check if batch is scanned and table has batch no field
		let batch_no_scan = Boolean(data.batch_no) && frappe.meta.has_field(cur_grid.doctype, "batch_no");

		if (batch_no_scan) {
			row_to_modify = this.get_batch_row_to_modify(data.batch_no);
		} else {
			// serial or barcode scan
			row_to_modify = this.get_row_to_modify_on_scan(row_to_modify, data);
		}

		if (!row_to_modify) {
      new_row = 1
			row_to_modify = frappe.model.add_child(this.frm.doc, cur_grid.doctype, 'items');
     
		}

		this.show_scan_message(row_to_modify.idx, row_to_modify.item_code);
		this.override_set_scanned_values(row_to_modify, data, scan_barcode_field,new_row);
	},
	get_row_to_modify_on_scan(row_to_modify, data) {
		// get an existing item row to increment or blank row to modify
		const existing_item_row = this.frm.doc.items.find(d => d.item_code === data.item_code);
		const blank_item_row = this.frm.doc.items.find(d => !d.item_code);

		if (existing_item_row) {
			row_to_modify = existing_item_row;
		} else if (blank_item_row) {
			row_to_modify = blank_item_row;
		}

		return row_to_modify;
	},
	override_set_scanned_values(row_to_modify, data, scan_barcode_field,new_row) {
		// increase qty and set scanned value and item in row
		// console.log("Child-------------->>")
		this.frm.from_barcode = this.frm.from_barcode ? this.frm.from_barcode + 1 : 1;
		frappe.model.set_value(row_to_modify.doctype, row_to_modify.name, {
			item_code: data.item_code,
			qty: (row_to_modify.qty || 0) + 1
		});
		
		['serial_no', 'batch_no', 'barcode'].forEach(field => {
			if (data[field] && frappe.meta.has_field(row_to_modify.doctype, field)) {
				let is_serial_no = row_to_modify[field] && field === "serial_no";
				let value = data[field];

				if (is_serial_no) {
					value = row_to_modify[field] + '\n' + data[field];
				}
				frappe.model.set_value(row_to_modify.doctype, row_to_modify.name, field, value);
			}
		});
    
    scan_barcode_field.set_value('');
		refresh_field("items");
    this.update_grid_ui(row_to_modify,new_row)

    
	},
  update_grid_ui(row_to_modify,new_row){
    if(new_row){
      let last_obj = this.frm.doc.items.pop()
      this.frm.doc.items.unshift(row_to_modify)
      let new_arr = this.frm.doc.items
      let count = 0
      this.frm.doc.items.forEach((item , index) => {
          item.idx = count +1;
          count++;
        })
    }
    
    refresh_field("items");
  },
	show_scan_message (idx, exist = null) {
		// show new row or qty increase toast
		if (exist) {
			frappe.show_alert({
				message: __('Row #{0}: Qty increased by 1', [idx]),
				indicator: 'green'
			});
		} else {
			frappe.show_alert({
				message: __('Row #{0}: Item added', [idx]),
				indicator: 'green'
			});
		}
	},
})


$.extend(
	cur_frm.cscript,
	new override_scan_code({frm: cur_frm}),
)


    // let old_row = frappe.model.copy_doc(row_to_modify)
    // old_row.idx = 1
    // new_arr.unshift(old_row)
    // console.log(new_arr)
    // this.frm.clear_table("items")
    // this.frm.doc.items = new_arr
 // var str = JSON.stringify(row_to_modify);
      // console.log(`-new--row_to_modify-->${row_to_modify}----str${str}`)
      // console.log(`-row_to_modify.idx-->${row_to_modify.idx}--`)
      // console.log(`-length-->${this.frm.doc.items.length}--`)
      // if (row_to_modify.idx>=1){
      //   const len_arr = this.frm.doc.items.length-1
      //   // for (let i =len_arr; i >=0; i--) {
      //   //   // console.log(`-length-->${len_arr}--`)
      //   //   // console.log(`-row shift-${i}->${this.frm.doc.items[i].item_code}--`)
      //   //   console.log(`- this.frm.doc.items[i]-==>${ this.frm.doc.items[i].idx}--`)
      //   //   this.frm.doc.items[i+1]  = this.frm.doc.items[i]
      //   //   this.frm.doc.items[i+1].idx  = i+1
      //   // }
      //   //   row_to_modify.idx = 1
      //   //   this.frm.doc.items[1] = row_to_modify
        
      //   // refresh_field("items");
      // }