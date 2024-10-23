
frappe.listview_settings['Sales Invoice'] = {
    onload: function(listview) {
        console.log(44444444444444)
        listview.page.add_action_item(__('Create Journal Entry'), function() {

            let selected_items = listview.get_checked_items();
            // console.log(selected_items)
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one item.'));
                return;
            }

            // Prompt user for confirmation before proceeding
            frappe.confirm(__('Are you sure you want to Create Journal Entries for the selected invoices?'), function() {
                selected_items.forEach(item => {
                    create_je(item.name);
                });
            });
        });
    }
};

function create_je(invoice_name) {
    frappe.call({
        method: "dynamic.alrehab.api.create_deferred_revenue_entry",
        args: {
            doc_name: invoice_name
        },
        callback: function(r) {
        }
    });
}