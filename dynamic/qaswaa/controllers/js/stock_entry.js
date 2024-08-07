frappe.ui.form.on('Stock Entry', {
    refresh: function (frm){

            frm.events.check_url(frm);
            console.log("hehehee");
    } ,
	// onload: function(frm) {
	// 	var entryType = frm.doc.stock_entry_type;
	// 	if (entryType === 'صرف هدايا') {
	// 		frappe.msgprint('ok');
			
	// 	}
	// },
	
       check_url: function (frm) {
        
            frappe.call({
                method: "dynamic.api.get_active_domains",
                callback: function (r) {
                    if (r.message && r.message.length) {
                        if (r.message.includes("Qaswaa")) {
                            frm.events.setup_button(frm);
                        }
                    }
                }
            })
        
    },
    setup_button: function(frm) {
		frappe.db.get_value("Stock Entry Type", {"matrial_type":"Dispensing Simples"},"name")
		.then(r => {
			var stock_entry_type = r.message.name;
		
        frm.add_custom_button(__('Stock Entry'),
			function() {
				if (!frm.doc.customer_id) {
					frappe.throw({
						title: __("Mandatory"),
						message: __("Please Select a Customer")
					});
				}
				erpnext.utils.map_current_doc({
					method: "dynamic.qaswaa.controllers.stock_entry.make_stock_entry",
					source_doctype: "Stock Entry",
					target: frm,
					setters: {
						customer_id: frm.doc.customer_id,
					},
					get_query_filters: {
						docstatus: 1,
						// status: ["not in", ["Closed", "On Hold"]],
						// per_delivered: ["<", 99.99],
						company: frm.doc.company,
						project: frm.doc.project || undefined,
                        mendatory_fields: 1,
						stock_entry_type : stock_entry_type				
					}
				})
			}, __("Get Items From"));
		})
    },
	stock_entry_type: function(frm) {
		frappe.call({
			method: "dynamic.api.get_active_domains",
			callback: function (r) {
				if (r.message && r.message.length) {
					if (r.message.includes("Qaswaa")) {
						frappe.db.get_value("Stock Entry Type", frm.doc.stock_entry_type , "matrial_type")
						.then(function(r) {
							let matrial_type = r.message.matrial_type;
							if (matrial_type == 'Dispensing Gift') {
								$(".custom-actions .inner-group-button").hide()
							}else{
								$(".custom-actions .inner-group-button").show()
							}
						});
					}
				}
			}
		})		
    }
});


