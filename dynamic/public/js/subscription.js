

frappe.ui.form.on('Subscription', {     
        /**
         * If the domain is "Rehab" :
            * It will add a button to the form to fetch all invoices if the status of the subscription is not 'Cancelled',
            * It will add a button to create a deferred revenue entry and update the invoice penalty if the subscription has invoices, 
         */
    refresh(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {
                    if(!frm.is_new()){
                        if(frm.doc.status !== 'Cancelled'){
                            frm.add_custom_button(__('Fetch All Invoices'), function() {
                                fetch_invoices(frm);
                            });
                        }

                        if(frm.doc.invoices.length != 0){
                            frm.add_custom_button(__('إنشاء قيد'), function() {
                                frm.events.calculateTotal(frm);
                                create_deferred_revenue_entry(frm);
                            });    
                        }
                    }
                }
            }}
        })        
    },
    // before_save:fetch unit area and set it on qty field
    before_save: function(frm) 
    {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {
                    let party= frm.doc.party;
                    if (party) {
                        frappe.db.get_value('Customer', party, 'unit_area', (r) => {
                        if (r && r.unit_area) {
                            frm.doc.plans.forEach((plan) => {
                                frappe.model.set_value(plan.doctype, plan.name, 'qty', r.unit_area);
                            });
                        }
                     });
                    }
                }
            }}
        })
    },
    
    calculateTotal(frm) {
        frappe.call({
            method: "dynamic.alrehab.api.set_total",
            args: {
                sub_id: frm.docname,
            },
            callback: function(r) {
                if (r.message) {
                }
            }
        });
    
    },
    update_invoice_penalty(frm){
        frappe.call({
            method: "dynamic.alrehab.api.update_sales_invoice_penalty",
            args: {
                    sub_id: frm.docname
             },
            callback: function(r) {
                console.log(r.message.status)
            }
        });
    }
});


  
function create_deferred_revenue_entry(frm) {
    frappe.call({
        method: "dynamic.alrehab.api.create_deferred_revenue_entry_group_of_invoices",
        args: {
            // doc_type: frm.doctype,
            // doc_name: frm.docname,
            invoices: frm.doc.invoices
        },
        callback: function(r) {
            if(r.message) {
                frappe.msgprint({
                    message: __('Deferred Revenue Entry for each invoice is created successfully.' ),
                })
            }
            else {
                frappe.msgprint(__('Failed to create Deferred Revenue Entry.'));
            }
        }
    });
}

function fetch_invoices(frm) {
    frappe.call({
        method: "dynamic.alrehab.subscription.get_subscription_updates_all_invoices",
        args: {
            name: frm.docname
        },
        callback: function(r) {
        }
    });
}

