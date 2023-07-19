// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stages RS Blocks', {
	refresh: function(frm) {
		frm.events.setup_quiries_fields(frm)
	},
	setup_quiries_fields:function(frm){
		frm.set_query("stage_name", function () {
			return {
			  filters: {
				project_name:frm.doc.project_name || null,
			  },
			};
		  });
		  
	}
});



cur_frm.fields_dict["items"].grid.get_field("unit_name").get_query = function(doc) {
	return {
		filters: {
		'reserved': 0,
		}

	}

}