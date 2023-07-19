// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt
frappe.provide("erpnext.stock");
frappe.provide("erpnext.accounts.dimensions");

{% include 'erpnext/stock/landed_taxes_and_charges_common.js' %};

frappe.ui.form.on('Repack', {
	setup:function(frm){
		frm.events.toggle_display(frm)
		frm.events.set_time(frm)
		
	},
	refresh:function(frm){
		frm.events.toggle_display(frm)
		frm.events.add_btn(frm)
		frm.events.set_time(frm)
		
	},
	set_time:function(frm){
		if(!frm.doc.posting_time){
			frm.set_value("posting_time", frappe.datetime.now_time());
		}
		if(!frm.doc.stock_entry_type){
			frm.set_value("stock_entry_type", 'Repack');
		}
	},
	set_posting_time:function(frm){
		frm.events.toggle_display(frm)
	},
	add_btn:function(frm){
		if(frm.doc.docstatus==1){
			frm.add_custom_button(
				__("Stock Entry"),
				function () {
				  frappe.model.open_mapped_doc({
					method:
					  "dynamic.dynamic.doctype.Repack.Repack.make_stock_entry",
					frm: frm, //this.frm
				  });
				},
				__("Create")
			  );
		}
	},
	toggle_display:function(frm){
		frm.set_df_property("posting_date", "read_only", !frm.doc.set_posting_time);
		frm.set_df_property("posting_time", "read_only", !frm.doc.set_posting_time);
		frm.refresh_fields('posting_date','posting_time')
	},
	from_warehouse: function(frm) {
		frm.trigger('set_transit_warehouse');
		set_warehouse_in_children(frm.doc.items, "s_warehouse", frm.doc.from_warehouse);
	},

	to_warehouse: function(frm) {
		set_warehouse_in_children(frm.doc.items, "t_warehouse", frm.doc.to_warehouse);
	},
	

	set_transit_warehouse: function(frm) {
		if(frm.doc.add_to_transit && frm.doc.purpose == 'Material Transfer' && !frm.doc.to_warehouse
			&& frm.doc.from_warehouse) {
			let dt = frm.doc.from_warehouse ? 'Warehouse' : 'Company';
			let dn = frm.doc.from_warehouse ? frm.doc.from_warehouse : frm.doc.company;
			frappe.db.get_value(dt, dn, 'default_in_transit_warehouse', (r) => {
				if (r.default_in_transit_warehouse) {
					frm.set_value('to_warehouse', r.default_in_transit_warehouse);
				}
			});
		}
	},
	get_items: function(frm) {
		if(!frm.doc.fg_completed_qty || !frm.doc.bom_no)
			frappe.throw(__("BOM and Manufacturing Quantity are required"));

		if(frm.doc.work_order || frm.doc.bom_no) {
			// if work order / bom is tioned, get items
			return frm.call({
				doc: frm.doc,
				freeze: true,
				method: "get_items",
				callback: function(r) {
					if(!r.exc) refresh_field("items");
					if(frm.doc.bom_no) attach_bom_items(frm.doc.bom_no)
				}
			});
		}
	},
});



function attach_bom_items(bom_no) {
	if (!bom_no) {
		return
	}

	if (check_should_not_attach_bom_items(bom_no)) return
	frappe.db.get_doc("BOM",bom_no).then(bom => {
		const {name, items} = bom
		erpnext.stock.bom = {name, items:{}}
		items.forEach(item => {
			erpnext.stock.bom.items[item.item_code] = item;
		});
	});
}

function check_should_not_attach_bom_items(bom_no) {
	return (
	  bom_no === undefined ||
	  (erpnext.stock.bom && erpnext.stock.bom.name === bom_no)
	);
  }

  function set_warehouse_in_children(child_table, warehouse_field, warehouse) {
	let transaction_controller = new erpnext.TransactionController();
	transaction_controller.autofill_warehouse(child_table, warehouse_field, warehouse);
}

  frappe.ui.form.on("Stock Entry Detail", "qty", function(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	if (row.qty > 0){
		frm.call({
			method:"dynamic.dynamic.doctype.Repack.Repack.get_row_qty",
			args:{
				"source_doc" :frm.doc,
				"item_code":row.item_code,
				"edit_row_qty":row.qty,
			},
			callback:function(r){
				let result = r.message
				if(result.flage==false){
					row.qty = result.qty
					frm.refresh_field('items')
					frappe.throw(__(result.msg))
				}
			}
		})
	}
  });
