frappe.provide('frappe.ui.form');

frappe.ui.form.CarQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
	init: function(doctype, after_insert, init_callback, doc, force) {
		this._super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	},

	render_dialog: function() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		this._super();
	},

	get_variant_fields: function() {
		var variant_fields = [
		{
			label: __("Plate Number"),
			fieldname: "plate_number",
			fieldtype: "Data"
		},
        {
			label: __("Device Type"),
			fieldname: "device_type",
			fieldtype: "Select",
			options: "\nGEBCO\nExternal\n"

		},
        {
			label: __("Customer"),
			fieldname: "customer",
			fieldtype: "Link",
			options: "Customer"

		},
        {
			label: __("Test"),
			fieldname: "test",
			fieldtype: "Data",
		},
		{
			fieldtype: "Column Break"
		},
		{
			label: __("Serial No"),
			fieldname: "serial_no",
			fieldtype: "Link",
			options: "Serial No"
		},
        {
			label: __("SIM Number"),
			fieldname: "sim_number",
			fieldtype: "Data",
		},
        {
			label: __("Customer Name"),
			fieldname: "customer_name",
			fieldtype: "Read Only",
            fetch_from:customer.customer_name
		},
		{
			fieldtype: "Section Break",
			label: __("Primary Address Details"),
			collapsible: 0
		},
		{
			label: __("Description"),
			fieldname: "description",
			fieldtype: "Small Text"
		},
		
		];

		return variant_fields;
	},
})
