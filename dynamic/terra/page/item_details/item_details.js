frappe.pages['item-details'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Item Details',
		single_column: true
	});
}