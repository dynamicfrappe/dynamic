frappe.ui.form.on("Material Request",{
    refresh(frm){

   
      frm.events.read_only_fields(frm)

        frm.events.trea_setup(frm)
        frappe.call({
          method: "dynamic.api.get_active_domains",
          callback: function (r) { 
            if (r.message && r.message.length) {
              if (r.message.includes("WEH")) {
                 frm.events.remove_cst_button(frm)
                 frm.events.read_only_fields(frm)
                 frm.events.remove_cst_button_create(frm)
          }
        }
        }
      })
    },
    on_submit:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
              if (r.message.includes("WEH")) {
                frappe.set_route('List', "Material Request", 'List')
              }
            }
          }
      })
    },
    after_save:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("WEH")) {
                  frm.events.remove_cst_button_create(frm)
                }
            }
        }
    })
    },
    read_only_fields:function(frm){
      frappe.call({
        method:"dynamic.weh.api.get_roles_hidden_field",
        args:{
          "field_hide":"material_request_read_only",
          "field_empty":"empty_source_warehouse_role",
        },
        callback:function(r) {
          frm.set_df_property("set_warehouse", "read_only", r.message.hide);
          if(r.message.empty){
            frm.set_value("set_from_warehouse","")
          }
          frm.refresh_fields("set_warehouse","set_from_warehouse")
        }
       })
    },
    trea_setup(frm){
        frappe.call({
          method:"dynamic.api.validate_terra_domain",
          callback:function(r) {
            if (r.message){
              frm.events.make_custom_buttons_2(frm)
            }
          }
         })
    
      },
    remove_cst_button:function(cur_frm){
      cur_frm.remove_custom_button(__("Bill of Materials"),__("Get Items From"))
      cur_frm.remove_custom_button(__('Sales Order'),__("Get Items From"))

    },
    remove_cst_button_create:function(frm){
      if (frm.doc.set_warehouse){
        frappe.call({
            method: 'dynamic.controllers.custom_item.get_users_warehouse',
            args: {
                warehouse:frm.doc.set_warehouse
            
            },
            callback: function(r) {
                if (r.message) {
                    const users = r.message.map(item => item.user);
                    if (!users.includes(frappe.session.user)) {
                        console.log("yes");
                        frm.remove_custom_button(__("Purchase Order"),__("Create"))
                        frm.remove_custom_button(__('Supplier Quotation'),__("Create"))
                        frm.remove_custom_button(__('Request for Quotation'),__("Create"))
                    }
                }
            }
        });
      }
    },
    make_custom_buttons_2: function(frm) {
        if (frm.doc.docstatus==1) {
            if (frm.doc.material_request_type === "Price Request") {
                frm.add_custom_button(__("Request for Quotation"),
                    () => frm.events.make_request_for_quotation_2(frm), __('Create'));
            }
            if (frm.doc.material_request_type === "Price Request") {
            frm.add_custom_button(__("Supplier Quotation"),
            () => frm.events.make_supplier_quotation_2(frm), __('Create')); }
        }
    },
    make_supplier_quotation_2: function(frm) {
		frappe.model.open_mapped_doc({
			method: "dynamic.terra.doctype.supplier_quotation.supplier_quotation.make_supplier_quotation",
			frm: frm
		});
    
    },
    make_request_for_quotation_2: function(frm) {
		frappe.model.open_mapped_doc({
			method: "dynamic.terra.doctype.supplier_quotation.supplier_quotation.make_request_for_quotation",
			frm: frm,
			run_link_triggers: true
		});
	},
  material_request_purpose:function(frm){
    
    if(frm.doc.material_request_purpose){
     
      frm.set_value('material_request_type',frm.doc.material_request_purpose)
      frm.refresh_field('material_request_type')
      frappe.call({
        "method" : "dynamic.weh.controllers.get_defaulte_source_warehouse",
        callback:function(r) {
          if (r.message) {
           frm.set_value("set_warehouse" , r.message[0]) 
           frm.refresh_field("set_warehouse")
           
          frm.set_query("set_warehouse", function(){
            return {
              "filters": [
                  ["Warehouse", "name", "in", r.message],
              
              ]
          }
          })

         if (r.message.length == 1){
          frm.set_df_property("set_warehouse", "read_only", 1);
          frm.refresh_field("set_warehouse")
         }
        }
        }
      })
    
    }
  }
    
    
})


const MaterialRequestController_Extend = erpnext.buying.MaterialRequestController.extend({
  refresh: function(doc){
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
          if (r.message && r.message.length) {
              if (r.message.includes("WEH")) {
                cur_frm.cscript['set_from_product_bundle'] = cur_frm.remove_custom_button(__('Product Bundle'),__("Get Items From"))
              }
          }
          else{
            this._super(doc);
          }
        }
      })

  }
  
})


$.extend(cur_frm.cscript, new MaterialRequestController_Extend({frm: cur_frm}));