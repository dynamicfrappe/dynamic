

frappe.listview_settings['Lead'] = {
    onload: function(listview) {

        listview.page.add_action_item(__('Approve Client Profiles'), function() {

            let selected_items = listview.get_checked_items();
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one item.'));
                return;
            }

            frappe.confirm(__('Are you sure you want to approve the selected client profiles?'), function() {
                selected_items.forEach(item => {
                    approve_leads(item);
                });
            });
        });
        listview.page.add_action_item(__('Reject Client Profiles'), function() {

            let selected_items = listview.get_checked_items();
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one item.'));
                return;
            }

            frappe.confirm(__('Are you sure you want to reject the selected client profiles?'), function() {
                selected_items.forEach(item => {
                    reject_leads(item);
                });
            });
        });
    }
};

function approve_leads(item) {
    frappe.call({
        method: "dynamic.true_lease.api.approve_leads",
        args: {
            name: item.name
        },
        callback: function(r) {
        }
    });
}

function reject_leads(item) {
    frappe.call({
        method: "dynamic.true_lease.api.reject_leads",
        args: {
            name: item.name
        },
        callback: function(r) {
        }
    });
}