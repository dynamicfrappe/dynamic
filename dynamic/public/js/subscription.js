

frappe.ui.form.on('Subscription', {
    setup(frm) {
        
    },
    onload(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {
                    frm.add_custom_button(__('إنشاء قيد'), function() {
                        create_deferred_revenue_entry(frm);
                    });
                    frm.add_custom_button(__('Fetch Invoices'), function() {
                        fetch_invoices(frm);
                    });
                    update_invoice_penalty(frm);
                    calculateTotal(frm);
                }
            }}
        })
    },
    after_save(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Rehab")) {
                    frm.add_custom_button(__('إنشاء قيد'), function() {
                        create_deferred_revenue_entry(frm);
                    });
                    frm.add_custom_button(__('Fetch Invoices'), function() {
                        fetch_invoices(frm);
                    });
                    update_invoice_penalty(frm);
                    calculateTotal(frm);
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
                        frm.refresh_field('plans');
                        }
                     });
                    }
                }
            }}
        })
    },
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
                var journal_entry_url = frappe.urllib.get_full_url('/desk/journal-entry/' + r.message.name);
                frappe.msgprint({
                    message: __('Deferred Revenue Entry created successfully: <a href="{0}" target="_blank">{1}</a>.' ).replace('{0}', journal_entry_url).replace('{1}', r.message.name),
                })
            }
            else {
                frappe.msgprint(__('Failed to create Deferred Revenue Entry.'));
            }
        }
    });
}

function update_invoice_penalty(frm){
    $.each(frm.doc.invoices || [], function (i, invoice) {
        frappe.call({
            method: "dynamic.alrehab.api.update_sales_invoice_penalty",
            args: {
                sales_invoice: invoice.invoice,
                penalty_value: frm.doc.penalty
            },
            callback: function(r) {

            }
        });
    });
}

function calculateTotal(frm) {
    var total = 0.0;
    $.each(frm.doc.invoices || [], function (i, invoice) {
        frappe.db.get_value('Sales Invoice', invoice.invoice , 'deferred_revenue_amount').then(r => {
            total = total + parseFloat(r.message.deferred_revenue_amount) ;

            frm.set_value('deferred_revenue_amount', total);

            frappe.call({
                method: "dynamic.alrehab.api.set_total",
                args: {
                   sub_id: frm.docname,
                   total: total
                },
                callback: function(r) {
                }
            });
        })
    });

}

function fetch_invoices(frm) {
    const doc = frm.doc;

    async function checkAndFetch() {

        if (new Date(doc.current_invoice_end) > new Date()) {
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