

frappe.listview_settings['Subscription'] = {
    onload: function(listview) {

        listview.page.add_action_item(__('Fetch Invoices'), function() {

            let selected_items = listview.get_checked_items();
            console.log(selected_items)
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one item.'));
                return;
            }

            // Prompt user for confirmation before proceeding
            frappe.confirm(__('Are you sure you want to fetch invoices for the selected subscriptions?'), function() {
                selected_items.forEach(item => {
                    console.log(item.name)
                    fetch_invoices(item);
                    calc_invoices_fine(item);
                });
            });
        });
    }
};

function calc_invoices_fine(item) {
    frappe.call({
        method: "dynamic.alrehab.api.update_sales_invoice_penalty",
        args: {
                sub_id: item.name
         },
        callback: function(r) {
            console.log(r.message.status)
        }
    });
    
    frappe.call({
        method: "dynamic.alrehab.api.set_total",
        args: {
            sub_id: item.name,
        },
        callback: function(r) {
            if (r.message) {
            }
        }
    });
}

function fetch_invoices(item) {
    frappe.call({
        method: "dynamic.alrehab.subscription.get_subscription_updates_all_invoices",
        args: {
            name: item.name
        },
        callback: function(r) {
        }
    });
}