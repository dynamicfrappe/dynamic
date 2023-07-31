

frappe.ui.form.on("Stock Reconciliation", {

    refresh(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Terra")) {
                        frm.events.set_queries_terra(frm)
                        if(frm.doc.docstatus < 1) {
                            frm.add_custom_button(__("Fetch Items from Warehouse"), function() {
                                frm.events.get_items(frm);
                            });
                        }
                    }
                }
            }
        })
    },
    set_queries_terra(frm) {
        frm.set_query('item_code','items', function(doc,cdt,cdn) {
            let row = locals[cdt][cdn]
            return{
                query: "dynamic.terra.api.get_item_group_brand",
                filters: { 
                    'item_group': row.item_group,
                    'brand': row.brand ,
                 }
               }
            })
    },
    get_items: function(frm) {
		let fields = [
			{
				label: 'Warehouse',
				fieldname: 'warehouse',
				fieldtype: 'Link',
				options: 'Warehouse',
				reqd: 1,
				"get_query": function() {
					return {
						"filters": {
							"company": frm.doc.company,
						}
					};
				}
			},
			{
				label: "Item Code",
				fieldname: "item_code",
				fieldtype: "Link",
				options: "Item",
				"get_query": function() {
					return {
						"filters": {
							"disabled": 0,
						}
					};
				}
			},
			{
				label: __("Ignore Empty Stock"),
				fieldname: "ignore_empty_stock",
				fieldtype: "Check"
			}
		];

		frappe.prompt(fields, function(data) {
			frappe.call({
				method: "erpnext.stock.doctype.stock_reconciliation.stock_reconciliation.get_items",
				args: {
					warehouse: data.warehouse,
					posting_date: frm.doc.posting_date,
					posting_time: frm.doc.posting_time,
					company: frm.doc.company,
					item_code: data.item_code,
					ignore_empty_stock: data.ignore_empty_stock
				},
				callback: function(r) {
					if (r.exc || !r.message || !r.message.length) return;

					frm.clear_table("items");

					r.message.forEach((row) => {
						let item = frm.add_child("items");
						$.extend(item, row);

						item.qty = item.qty || 0;
						item.valuation_rate = item.valuation_rate || 0;
					});
					frm.refresh_field("items");
				}
			});
		}, __("Get Items"), __("Update"));
	},


})




