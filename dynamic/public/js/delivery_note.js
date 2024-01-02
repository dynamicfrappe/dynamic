


frappe.ui.form.on("Delivery Note", {
    domian_valid: function (frm) {
        var tera = false
       frappe.call({
             method :"dynamic.dynamic.validation.get_active_domain_gebco" ,
             async: false,
             callback:function (r){
                 if (r.message) {
                     tera = true
                 }else {
                     tera = false
                 }
             }
         })
      return tera
 
     } ,
     onload(frm) {
        var check_domain = frm.events.domian_valid()
        if (check_domain && frm.doc.docstatus == 0) {
            frm.add_custom_button(
              __("view Item Shortage"),
              function () {
                frappe.call({
                  method:
                    "dynamic.api.validate_active_domains_note",
                  args: {
                    doc: frm.doc.name ,
                  },
                  callback: function (r) {
                     console.log(r.message);
                    
                    // socket(JSON.stringify(data));
                  },
                });
              },
              "view Item Shortage"
            );
          }

     } ,  

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
                      if (frm.doc.set_warehouse || local.warehouse ) {
                      
                        var args = {"item" : local.item_code ,
                        "s_warehouse" :local.warehouse || frm.doc.set_warehouse ,
                       
                       }
                        if (!frm.__islocal) {
                          console.log("Old Document !")
                          args = {"item" : local.item_code ,
                                  "s_warehouse" :local.warehouse || frm.doc.set_warehouse ,
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
                          }
                        })
                      }
                     
    
    
    
    
                  }
              }
          }
      })
      }
  
    
})



frappe.ui.form.on("Delivery Note Item", { 
    stock_uom_rate:function(doc,cdt,cdn){
        var row = locals[cdt][cdn]
        if(row.stock_uom_rate){
            row.rate = row.stock_uom_rate * row.conversion_factor
            row.price_list_rate = row.stock_uom_rate * row.conversion_factor
        }
        cur_frm.refresh_fields("items")
    },
    item_code:function(frm ,cdt , cdn){
        frm.events.item_code_update(frm ,cdt , cdn)
      },
      warehouse:function(frm ,cdt , cdn){
        
        frm.events.item_code_update(frm ,cdt , cdn)
      },
})
//******* */
const override_scan_code = erpnext.stock.DeliveryNoteController.extend({
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
            // add new row if new item/batch is scanned
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
        // var reversed = this.frm.doc.items.reverse();
        // let count = 0
        // reversed.forEach((item , index) => {
        //   item.idx = count +1;
        //   count++;
        // })
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