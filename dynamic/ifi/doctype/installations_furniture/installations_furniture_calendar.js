
// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Installations Furniture"] = {
	field_map: {
		"start": "from_time",
		"end": "to_time",
		"id": "name",
		"title": "name",
		"allDay": "allDay"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "sales_order",
			"options": "Sales Order",
			"label": __("Sales Order")
		},
	],
	get_events_method: "dynamic.ifi.doctype.installations_furniture.installations_furniture.get_events",
	get_css_class: function(data) {
        console.log(data)
		if(data.ref_status=="Pending") {
			return "success";
		} if(data.ref_status=="Start") {
			return "danger";
		} else if(data.ref_status=="Inprogress") {
			return "warning";
		} else if(data.ref_status=="Completed") {
			return "extra-light";
		}
	}
}
