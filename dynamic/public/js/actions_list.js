

frappe.listview_settings['Actions'] = {
    onload: function(listview) {

        listview.page.add_action_item(__('Approve Actions'), function() {

            let selected_items = listview.get_checked_items();
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one item.'));
                return;
            }

            frappe.confirm(__('Are you sure you want to approve the selected actions?'), function() {
                selected_items.forEach(item => {
                    approve_actions(item);
                });
            });
        });
        listview.page.add_action_item(__('Reject Actions'), function() {

            let selected_items = listview.get_checked_items();
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one item.'));
                return;
            }

            frappe.confirm(__('Are you sure you want to reject the selected actions?'), function() {
                selected_items.forEach(item => {
                    reject_actions(item);
                });
            });
        });
    }
};

function approve_actions(item) {
    frappe.call({
        method: "dynamic.true_lease.api.approve_actions",
        args: {
            name: item.name
        },
        callback: function(r) {
        }
    });
}

function reject_actions(item) {
    frappe.call({
        method: "dynamic.true_lease.api.reject_actions",
        args: {
            name: item.name
        },
        callback: function(r) {
        }
    });
}