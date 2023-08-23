// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project RS Stages', {
	// setup: function(frm) {
		
	// }
});



cur_frm.fields_dict["items"].grid.get_field("block_name").get_query = function(doc) {
	return {
		filters: {
		'project_name': doc.project_name,
		'stage_name': doc.stage_name,
		}

	}

}