frappe.ui.form.on("Sales Invoice", {
	setup(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Cheques")) {
							frm.custom_make_buttons["Cheque"] = "Cheque";
					}
			}}
	})
	},
	domian_valid: function (frm) {
		var tera = false;
		frappe.call({
			method: "dynamic.dynamic.validation.get_active_domain_gebco",
			async: false,
			callback: function (r) {
				if (r.message) {
					tera = true;
				} else {
					tera = false;
				}
			},
		});
		return tera;
	},
	// onload(frm) {
	//   var check_domain = frm.events.domian_valid();
	//   // console.log(check_domain)
	//   if (check_domain && frm.doc.docstatus == 0) {
	//     frm.add_custom_button(
	//       __("view Item Shortage"),
	//       function () {
	//         frappe.call({
	//           method: "dynamic.api.validate_active_domains_invocie",
	//           args: {
	//             doc: frm.doc.name,
	//           },
	//           callback: function (r) {
	//             console.log(r.message);
	//           },
	//         });
	//       },
	//       "view Item Shortage"
	//     );
	//   }
	// },
 toggle_read_only_fields(frm) {
	// frm.set_df_property('items', 'read_only', 1);
	cur_frm.fields_dict.items.grid.update_docfield_property(
		"item_code",
		"read_only",
		1
	);
	
},

get_update_btn:function(frm){

	frappe.call({
		method: "dynamic.alrehab.api.get_updates",
		args:{
				"name": frm.docname,
		}, 
		callback: function (r) {
				if (r.message && r.message.length) {
						console.log("lllllllllllll")
				}
		}
})

},

	onload(frm) {

		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Rehab")) {
						frm.add_custom_button(__('إنشاء قيد'), function() {
							frm.refresh_fields();
							create_deferred_revenue_entry(frm);
						});
					}
			}}

		})

		var check_domain = frm.events.domian_valid(); 
		
		if (check_domain && frm.doc.docstatus == 0) {
				
				frm.add_custom_button(
						__("view Item Shortage"),  
						function () {
								frappe.call({
										method: "dynamic.api.validate_active_domains_invocie", 
										args: {
												doc: frm.doc.name  
										},
										callback: function (r) {
												console.log(r.message);  
										}
								});
						},
						"view Item Shortage" 
				);
		} else {
			// frappe.call({
			//     method: "dynamic.api.get_active_domains", 
			//     callback: function(r) {
			//         if (r.message && r.message.includes("Qaswaa")) {
			//             console.log("baio");
			//             if (frm.doc.is_return == 1) {
			//                 console.log("ddds");
			//                 frm.set_df_property('sales_team', 'read_only', 1);
			//                 frm.set_df_property('tax', 'read_only', 1);
			//                 frm.trigger("toggle_read_only_fields");
			//                 frm.refresh_field('sales_team');
			//                 frm.refresh_field('tax');
			//                 frm.refresh_field('items');
			//             }
			//         }
			//     }
			// });
	}
	}, 
	


	refresh(frm) {
		frm.events.add_cheque_button(frm);
		frm.events.set_query(frm)
		frm.events.upload_data_file(frm)
		// const myTimeout = setTimeout(get_customer_query, 1300);
		var check_domain = frm.events.domian_valid();
		if (check_domain && frm.doc.docstatus == 0) {
			frm.add_custom_button(
				__("view Item Shortage"),
				function () {
					frappe.call({
						method: "dynamic.api.validate_active_domains_invocie",
						args: {
							doc: frm.doc.name,
						},
						callback: function (r) {
							console.log(r.message);
						},
					});
				},
				"view Item Shortage"
			);
			
		}
		frappe.call({
			method: "dynamic.api.get_active_domains", 
			callback: function(r) {
					if (r.message && r.message.includes("Qaswaa")) {
							if (frm.doc.is_return == 1) {
									frm.set_df_property('sales_team', 'read_only', 1);
									frm.set_df_property('taxes', 'read_only', 1);
									frm.trigger("toggle_read_only_fields");

									$.each(frm.fields_dict, function(fieldname, field) {
										frm.set_df_property(fieldname, 'read_only', 1);
									});
									frm.set_df_property('set_warehouse', 'read_only', 0);
									frm.set_df_property('items', 'read_only', 0);
									// cur_frm.set_df_property('items' , 'qty' , 'read_only' , 0);
							}
					}
			}
	});
		
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
	brand:function(frm){
		frm.fields_dict.items.grid.get_field("item_code").get_query = function () {
			return {
				filters: [
					["brand", "=", cur_frm.doc.brand],
				],
			};
		};
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
						console.log("Catech !!")
						frm.events.add_item_discount_rate(frm);
					}
				}
			}
		});
	},



	add_cheque_button(frm) {
		if (frm.doc.docstatus == 1) {
			frappe.call({
				method: "dynamic.api.get_active_domains",
				callback: function (r) {
					if (r.message && r.message.length) {
						if (r.message.includes("Cheques")) {
							if (
								frm.doc.outstanding_amount != 0 &&
								!(cint(frm.doc.is_return) && frm.doc.return_against)
							) {
								frm.add_custom_button(
									__("Cheque"),
									function () {
										frm.events.make_cheque_doc(frm);
									},
									__("Create")
								);
							}
						}
					}
				},
			});
		}
	},
	make_cheque_doc(frm) {
		return frappe.call({
			method: "dynamic.cheques.doctype.cheque.cheque.make_cheque_doc",
			args: {
				dt: frm.doc.doctype,
				dn: frm.doc.name,
			},
			callback: function (r) {
				var doc = frappe.model.sync(r.message);
				frappe.set_route("Form", doc[0].doctype, doc[0].name);
			},
		});
	},
	cost_center:function(frm){
		if(frm.doc.cost_center){
			frappe.call({
				method: "dynamic.api.get_active_domains",
				callback: function (r) {
					if (r.message && r.message.length) {
						if (r.message.includes("Cost Center")) {
								$.each(frm.doc["items"] || [], function(i, item) {
									item.cost_center = flt(frm.doc.cost_center);
								});
								frm.refresh_field("items");
							}
							if (r.message.includes("Qaswaa")) {
								frappe.db.get_value('Cost Center', frm.doc.cost_center, 'is_default')
									.then(r => {
											if(r.message.is_default == 1){
												frm.set_df_property('update_stock', 'read_only', 0);
											}else{
												frm.set_df_property('update_stock', 'read_only', 1);
												frm.set_value('update_stock', 1);
												frm.refresh_field('update_stock');
											}
									})
								
							}
						}
					}
			})
	}
		
	},
	set_discount:function(frm){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length && r.message.includes("Healthy Corner")) {
					frm.doc.items.forEach(item => {
						if (item.qty) {
							item.discount_percentage = frm.doc.discount_item ; 
						}
					});			
				}
			}
		}); 
	}

});


function create_deferred_revenue_entry(frm) {
	frappe.call({
			method: "dynamic.alrehab.api.create_deferred_revenue_entry",
			args: {
					doc_name: frm.docname,
			},
			callback: function(r) {
					if(r.message) {
							frappe.msgprint({
									message: __('Deferred Revenue Entry created successfully:{1} ' ).replace('{1}', r.message.name),
							})
					}
					else {
							frappe.msgprint(__('Failed to create Deferred Revenue Entry.'));
					}
			}
	});
}

function get_customer_query(){
	frappe.call({
		method: "dynamic.api.get_active_domains",
		callback: function (r) {
			if (r.message && r.message.length) {
				if (r.message.includes("Master Deals")) {
					cur_frm.set_query('customer',(doc)=>{
						return {
							query: 'dynamic.master_deals.master_deals_api.customer_query_custom',
							filters:{"docname":cur_frm.doc.name}
						}
						
					})
				}
			}
		},
	});
	
}


// frappe.ui.form.on("Sales Team", {
//   sales_person:function(frm,cdt,cdn){
//     frappe.call({
//       method: "dynamic.api.get_active_domains", 
//       callback: function(r) {
//           if (r.message && r.message.includes("Qaswaa")) {
//               console.log("ee");
//               if (frm.doc.is_return == 1) {
//                   console.log("ee");
//                   frm.set_df_property("sales_person", "read_only", 1);    
//                   frm.refresh_field('sales_person'); 
//               }
//           }
//       }
//   });
//   }

// })





frappe.ui.form.on("Sales Invoice Item", {
	items_add: function(frm,cdt,cdn) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length && r.message.includes("Healthy Corner")) {

					// get_discount_item_from_customer(frm , cdt , cdn);
					total_before_discount(frm);
					// total_discount(frm);					
				}
			}
		}); 
		
},
	item_code:function(frm,cdt,cdn){
		console.log("Catshed ")
		let row = locals[cdt][cdn]
		if(row.item_code){

		 
			frappe.call({
				method: "dynamic.api.get_active_domains",
				callback: function (r) {
						if (r.message && r.message.length && r.message.includes("Qaswaa")) {

							var item_discount_rate = frm.doc.item_discount_rate;
								console.log(item_discount_rate);
								if (item_discount_rate ){
								row.discount_percentage = item_discount_rate
								// frm.set_value("items","discount_percentage",item_discount_rate)
							 
								frm.refresh_fields("items");
				 }
						}
				}
		}); 

		
			
		}
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length && r.message.includes("Healthy Corner")) {
					
					total_before_discount(frm);
					// total_discount(frm);
					
					setTimeout(() => {
						get_discount_item_from_customer(frm , cdt , cdn);
					  }, "1000");
				}
			}
		}); 
	},
	qty:function(frm,cdt,cdn){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function(r) {
				if (r.message && r.message.length && r.message.includes("Healthy Corner")) {
					set_all_price_before_discount(frm, cdt, cdn)
					.then(() => {
						total_before_discount(frm);
						// total_discount(frm);
					});
				}
			}
		});
	},
	rate:function(frm , cdt , cdn){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length && r.message.includes("Healthy Corner")) {
					total_before_discount(frm);
					// total_discount(frm);
				}
			}
		}); 
	},
	item_remove:function(frm,cdt,cdn){
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length && r.message.includes("Healthy Corner")) {
					total_before_discount(frm);
					// total_discount(frm);
					console.log("removed");
								
				}
			}
		}); 
	},

})

function set_all_price_before_discount(frm, cdt, cdn) {
    return new Promise((resolve, reject) => {
        let row = locals[cdt][cdn];

        if (row.item_code) {
            if (row.qty && row.conversion_factor) {
                let stock_qty = row.qty * parseFloat(row.conversion_factor);
                let base_price_list_rate = parseFloat(row.base_price_list_rate) || 0;
                let item_price = base_price_list_rate * stock_qty;

                frappe.model.set_value(cdt, cdn, 'total_item_price', item_price);
                resolve();
            } else {
                reject("Quantity or conversion factor is missing");
            }
        } else {
            reject("Item code is missing");
        }
    });
}

function total_before_discount(frm) {
    let total_price = 0;

    frm.doc.items.forEach(item => {
        if (item.total_item_price) {
            total_price += item.total_item_price;
        }
    });
	let temp = parseFloat(frm.doc.total) - parseFloat(total_price)
	console.log("temp ======>",temp);
    frm.set_value("total_price", total_price);
	frm.set_value("discount" , temp)
    frm.refresh_field("total_price");
	frm.refresh_field("discount");
}

function total_discount(frm) {
    let total_discount = 0;

    frm.doc.items.forEach(item => {
        if (item.discount_amount) {
            total_discount += parseFloat(item.qty) * parseFloat(item.conversion_factor) * parseFloat(item.discount_amount);
        }
    });

    frm.set_value("discount", total_discount);
    frm.refresh_field("discount");
}

function get_discount_item_from_customer(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    frappe.call({
        method: "dynamic.api.get_active_domains",
        callback: function(r) {
            if (r.message && r.message.length && r.message.includes("Healthy Corner")) {
                if (frm.doc.customer) {
                    frappe.db.get_value('Customer', frm.doc.customer, 'discount_item')
                        .then(r => {
                            let discount_item = parseFloat(r.message.discount_item || 0);
                            console.log(discount_item);

                            
							row.discount_percentage = discount_item;
							
							row.rate =  row.price_list_rate -( (discount_item / 100) * row.price_list_rate) ;


                            frm.refresh_field("items");
							
							
							console.log("Updated:", row);
                        });
                }
            }
        }
    });
}



const extend_sales_invoice = erpnext.accounts.SalesInvoiceController.extend({
	refresh: function(doc, dt, dn) {
		const me = this;
		this._super(doc,dt,dn);
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					// console.log('domains ',r.message)
					if(r.message.includes("Qaswaa")){
						// sales invoice
						if (doc.docstatus == 1 && doc.outstanding_amount!=0
							&& !(cint(doc.is_return) && doc.return_against)) {
								cur_frm.cscript['make_payment_entry'] = create_payment_sales_person //new
								// cur_frm.page.remove_inner_button('Payment', 'Create')
						}
				 
					}
				}
			}
		})

		
	},
	

	
})

$.extend(
	cur_frm.cscript,
	new extend_sales_invoice({frm: cur_frm}),
);


var create_payment_sales_person = function() {
	return frappe.call({
		method: "dynamic.qaswaa.utils.qaswaa_api.get_payment_entry",
		args: {
			'dt': cur_frm.doc.doctype,
			'dn': cur_frm.doc.name
		},
		callback: function(r) {
			var doc = frappe.model.sync(r.message);
			frappe.set_route('Form', doc[0].doctype, doc[0].name);
		}
	});
	// frappe.model.open_mapped_doc({
	//   method: "dynamic.qaswaa.utils.qaswaa_api.get_payment_entry",
	//   frm: cur_frm
	// })
}