// Copyright (c) 2023, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project RS', {
	setup: function (frm) {
		frm.custom_make_buttons = {
			"Create Stage": "Project RS Stages", //"Additional Salary" name of button: "Additional Salary" name of doctype in dashboard .py,
		};
	},
	refresh: function(frm) {
		frm.add_custom_button("Create Stage", () => {
			frm.events.create_stage(frm)
		},"Create"
		)
	},
	create_stage:function(frm){
		frappe.model.open_mapped_doc({
			method:"dynamic.real_state.doctype.project_rs.project_rs.create_stage",
			frm:frm,
			args:{
				"project_name":frm.doc.project_name,
			}
		})
	}
});



cur_frm.fields_dict["stages"].grid.get_field("stage_name").get_query = function(doc) {
	return {
		filters: {
		'project_name': doc.project_name,
		}

	}

}