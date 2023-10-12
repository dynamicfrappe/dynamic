

frappe.ui.form.on("Stock Reconciliation", {

    refresh(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Terra")) {
                        frm.events.set_queries_terra(frm)
                        if(frm.doc.docstatus < 1) {
							cur_frm.remove_custom_button('Fetch Items from Warehouse')
                            frm.add_custom_button(__("Fetch Items from Warehouse"), function() {
                                frm.events.get_items(frm);
                            });
                        }
                    }
                }
            }
        }),
		frm.fields_dict["items"].grid.add_custom_button(
			__("Excel Upload"),
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
				  console.log(values);
				  var f = values.first_name;
				  frappe.call({
					method: "dynamic.api.add_stcok_reconciliation",
					args: {
					  file: values.first_name,
					},
					callback: function(r) {
					  if (r.message) {
						frm.clear_table("items");
						frm.refresh_fields("items");
						// console.log(r.message)
						r.message.forEach((element) => {
						  var row = frm.add_child("items");
						  row.item_code = element.Item_Code;
						  row.warehouse = element.Warehouse;
						  row.item_name = element.Item_Name;
						  row.qty = element.Quantity;
						  row.valuation_rate = element.Valuation_Rate;
						  row.brand = element.brand;
						  row.item_group = element.item_group;
						  row.serial_no = element.Serial_No;
						  row.batch_no = element.Batch_No;
						});
						frm.refresh_fields("items");
					  }
					},
				  });
				  d.hide();
				},
			  });
	  
			  d.show();
			}
		  );
		  frm.fields_dict["items"].grid.grid_buttons
		  .find(".btn-custom")
		  .removeClass("btn-default")
		  .addClass("btn-primary");
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
				method: "dynamic.terra.api.get_items",
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




