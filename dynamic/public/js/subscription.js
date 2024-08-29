

frappe.ui.form.on('Subscription', {
    refresh(frm){
        frm.events.add_custom_button_fetch_invoices(frm);
        if(frm.doc.invoices.length != 0){
            frm.events.update_invoice_penalty(frm);
            frm.events.calculateTotal(frm);
            if(frm.doc.deferred_revenue_amount){
                frm.events.add_custom_button_create_je(frm);
            }
        }
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
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {
                    frm.add_custom_button(__('Fetch All Invoices'), function() {
                        fetch_invoices(frm);
                    });
                }
            }}
        })
    },
    add_custom_button_create_je(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {
                    frm.add_custom_button(__('إنشاء قيد'), function() {
                        create_deferred_revenue_entry(frm);
                    });
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
                    frm.doc.set_value("deferred_revenue_amount", r.message.total);
                    frm.doc.refresh()
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
        method: "dynamic.alrehab.api.create_deferred_revenue_entry",
        args: {
            doc_type: frm.doctype,
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

function fetch_invoices(frm) {
    const doc = frm.doc;

    async function checkAndFetch() {
        // Convert the current_invoice_end to YYYYMMDD format
        const [endYear, endMonth, endDay] = doc.current_invoice_end.split("-");
        const currentInvoiceEndFormatted = `${endYear}${endMonth.padStart(2, '0')}${endDay.padStart(2, '0')}`;

        // Get today's date in YYYYMMDD format
        const today = new Date();
        const todayYear = today.getFullYear();
        const todayMonth = String(today.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        const todayDay = String(today.getDate()).padStart(2, '0');
        const todayFormatted = `${todayYear}${todayMonth}${todayDay}`;

        console.log("Current Invoice End Date (Original):", doc.current_invoice_end);
        console.log("Formatted Current Invoice End Date (YYYYMMDD):", currentInvoiceEndFormatted);
        console.log("Today's Date (YYYYMMDD):", todayFormatted);

        // Compare the formatted dates
        if (currentInvoiceEndFormatted >= todayFormatted) {
            console.log("Invoice end date is in the future. Stopping the function.");
            return;
        }
        
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
    
    checkAndFetch();
}
