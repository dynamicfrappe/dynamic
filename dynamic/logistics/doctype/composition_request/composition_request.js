// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Composition Request', {
	refresh : function(frm){
		frm.set_query("sales_order", () => {
			return { filters: {"docstatus" : 1}};
		});
		frm.set_query("survey", () => {
			return { filters:[["type", "=", frm.doc.doctype]],
			};
		});
	},
	survey : function(frm){
		frm.call({
			doc: frm.doc,
			method: "fetch_survey_template",
			args : {survey :frm.doc.survey},
			callback: function (r) {
				
				refresh_fields("survey_template")
			},
		});
	},
	sales_order: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.call({
							doc : frm.doc ,
							method: "get_items",
							callback: function (r) {
								frm.doc.items = []
								r.message.forEach(element => {
									frm.add_child("items" , element);
								});
								frm.refresh_fields("items");
							},			 
						})	
					}
				}
			}
		})
	},
	customer: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Logistics")) {
						frm.call({
							doc : frm.doc ,
							method: "set_address_and_numbers",	 
						})	
					}
				}
			}
		})
	}

});

frappe.ui.form.on("Sales Order Item", {

	add_serial_no: function(frm , cdt , cdn ){
		let row = locals[cdt][cdn]
		frappe.call({
		  method: "dynamic.api.get_active_domains",
		  callback: function (r) {
			if (r.message && r.message.length) {
			  if (r.message.includes("Logistics")) {
	
				let d = new frappe.ui.Dialog({
				  title: "Select Serial Numbers",
				  fields: [
					
					{
					  label: "Item Code",
					  fieldname: "item_code",
					  fieldtype: "Link",
					  options: "Item",
					  default : row.item_code,
					  onchange: () => {
						row.item_code =  d.fields_dict.item_code.get_value();
						frm.refresh_field("items");
					  }
					},
					{
					  label: "Warehouse",
					  fieldname: "warehouse",
					  fieldtype: "Link",
					  options: "Warehouse",
					  reqd: 1,
					  default : row.warehouse,
					  onchange: () => {
						row.warehouse =  d.fields_dict.warehouse.get_value();
						frm.refresh_field("items");
					  }
	
					},
					{fieldtype:"Column Break"},
					{
					  label: "Qty",
					  fieldname: "qty",
					  fieldtype: "Int",
					  default: 0.0,
					  default : row.qty,
					  onchange: () => {
						row.qty =  d.fields_dict.qty.get_value();
						frm.refresh_fields("items");
					  }
					  
					},
					{
					  label: "UOM",
					  fieldname: "uom",
					  fieldtype: "Link",
					  options: "UOM",
					  default : row.uom,
					  onchange: () => {
						row.uom =  d.fields_dict.uom.get_value();
						frm.refresh_fields("items");
					  }
					},
					{
					  label: "Auto Fetch",
					  fieldname: "auto_fetch",
					  fieldtype: "Button",
					  click: () => {
						let qty = d.fields_dict.qty.get_value();
						let warehouse = d.fields_dict.warehouse.get_value();
						let item_code = d.fields_dict.item_code.get_value();
						row.qty = qty
						if(item_code && warehouse && qty > 0){
							row.serial = ""
							frm.refresh_fields("items"); 
						  frm.call({
							method:'dynamic.logistics.logistics_api.fetch_serial_numbers',
							args:{
							  item_code:item_code,
							  warehouse : warehouse,
							  qty : qty,
							},
							callback:function(r){
								if(!r.message){
						  			frappe.throw(("This Itme not has serial no  "))
								}
								if(r.message){
									row.serial = r.message
									frm.refresh_fields("items"); 
								}
							}
						  })
						}
						else if(!item_code){
						  frappe.throw(("please define item code"))
						}
						else if(!warehouse){
						  frappe.throw(("please define warehouse"))
						}
						else if(qty <= 0){
						  frappe.throw(("please define qty"))
						}
					  }
					},
				  ],
				  primary_action_label: "Submit",
				  primary_action(values) {
					frm.refresh_fields("items");
		  
					d.hide();
				  },
				});
		  
		  
				d.show();
	
			  }
			}
		  }
		});
	  },
})