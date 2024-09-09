

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
            frappe.confirm(__('Are you sure you want to fetch invoices for the selected items?'), function() {
                console.log(123)
                selected_items.forEach(item => {
                    console.log(item)
                    fetch_invoices(item);
                });
            });
        });
    }
};



function fetch_invoices(item) {

    async function checkAndFetch() {

        const dateResponse = await frappe.call({
            method: "dynamic.alrehab.api.get_date",
            args: {
                doc_type: item.name
            }
        });
        
        if (dateResponse.message) {
            return;
        }
        else{
            
            await frappe.call({
                method: "erpnext.accounts.doctype.subscription.subscription.get_subscription_updates",
                args: { name: item.name },
                freeze: true,
                callback: function (data) {
                    if (!data.exc) {
                        item.reload_doc();

                    }
                }
            });
            
            await new Promise(resolve => setTimeout(resolve, 5000));
            
            checkAndFetch();
        }
    }
    
    checkAndFetch();
}