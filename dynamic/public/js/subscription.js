

frappe.ui.form.on('Subscription', {
    refresh(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {

                    frm.events.add_custom_button_fetch_invoices(frm);
                    
                    if(frm.doc.invoices.length != 0){
                        frm.events.update_invoice_penalty(frm);
                        frm.events.calculateTotal(frm);
                        if(frm.doc.deferred_revenue_amount){
                            frm.events.add_custom_button_create_je(frm);
                        }
                    }
                
                }
            }}
        })        
    },

    before_save: function(frm) {
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
    add_custom_button_fetch_invoices(frm){
        frm.add_custom_button(__('Fetch All Invoices'), function() {
            fetch_invoices(frm);
        });
    },
    add_custom_button_create_je(frm){
        frm.add_custom_button(__('إنشاء قيد'), function() {
            create_deferred_revenue_entry(frm);
        });
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
            doc_type: frm.doctype,
            doc_name: frm.docname,
        },
        callback: function(r) {
            if(r.message) {
                frappe.msgprint({
                    message: __('Deferred Revenue Entry for each invoice are created successfully.' ),
                })
            }
            else {
                frappe.msgprint(__('Failed to create Deferred Revenue Entry.'));
            }
        }
    });
}

function fetch_invoices(frm) {

    async function checkAndFetch() {
        
        const doc = frm.doc;

        const dateResponse = await frappe.call({
            method: "dynamic.alrehab.api.get_date",
            args: {
                doc_type: frm.doc.name
            }
        });
        
        if (dateResponse.message) {
            return;
        }
        else{
            
            await frappe.call({
                method: "erpnext.accounts.doctype.subscription.subscription.get_subscription_updates",
                args: { name: doc.name },
                freeze: true,
                callback: function (data) {
                    if (!data.exc) {
                        frm.reload_doc();

                    }
                }
            });
            
            await new Promise(resolve => setTimeout(resolve, 5000));
            
            checkAndFetch();
        }
    }
    
    checkAndFetch();
}

// function fetch_invoices(frm) {

//     async function checkAndFetch() {
        
//         const doc = frm.doc;

//         try {
//             const dateResponse = await frappe.call({
//                 method: "dynamic.alrehab.api.get_date",
//                 args: {
//                     doc_type: frm.doc.name
//                 }
//             });

//             if (dateResponse.message) {
//                 console.log('Date Response:', dateResponse.message);
//             } else {
//                 console.log('Unexpected Response:', dateResponse.message);
//                 console.log(555);
//             }

//             const subscriptionResponse = await frappe.call({
//                 method: "erpnext.accounts.doctype.subscription.subscription.get_subscription_updates",
//                 args: { name: doc.name },
//                 freeze: true
//             });

//             if (!subscriptionResponse.exc) {
//                 await frm.reload_doc();
//             }

//         } catch (error) {
//             console.error('Error during fetching:', error);
//         }

//         await new Promise(resolve => setTimeout(resolve, 5000));

//         // Exit condition (example: stop after certain attempts)
//         if (some_exit_condition) {
//             return;
//         }

//         checkAndFetch();
//     }

//     checkAndFetch();
// }
