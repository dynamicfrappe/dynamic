frappe.ui.form.on("Material Request",{
    refresh(frm){
        frm.events.trea_setup(frm)
        frm.events.remove_cst_button(frm)
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
    remove_cst_button:function(frm){
      frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function (r) {
            if (r.message && r.message.length) {
                if (r.message.includes("WEH")) {
                  frm.remove_custom_button(__("Bill of Materials"),__("Get Items From"))
                  frm.remove_custom_button(__('Sales Order'),__("Get Items From"))
                }
            }
          }
        })
      
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
  
    
    
})

frappe.provide("erpnext.buying");

const MaterialRequestController_Extend = erpnext.buying.BuyingController.extend({
  refresh: function(doc){
    frappe.call({
      method: "dynamic.api.get_active_domains",
      callback: function (r) {
          if (r.message && r.message.length) {
              if (r.message.includes("WEH")) {
                frappe.dynamic_link = {doc: doc, fieldname: 'supplier', doctype: 'Supplier'};
                this.cur_frm.toggle_display("supplier_name",
                  (doc.supplier_name && doc.supplier_name!==doc.supplier));
                this.toggle_subcontracting_fields();
              }
          }
          else{
            this._super();
          }
        }
      })
    // this._super(doc);
		
		// 
    
  }
  
})


$.extend(cur_frm.cscript, new MaterialRequestController_Extend({frm: cur_frm}));