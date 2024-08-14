

frappe.ui.form.on("Actions", {

    refresh: function (frm) {  
        frm.events.add_assign_to_button(frm);
    
    },

    add_assign_to_button(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("True lease")) {
                    frm.add_custom_button( __("Assign To"), () => {
                            var d = new frappe.ui.Dialog({
                                title: __("Assign To Departments"),
                                fields: [
                                    {
                                        label: __("Departments"),
                                        fieldname: "departments",
                                        fieldtype: "MultiSelectList",
                                        get_data: function(txt) {
                                            return frappe.db.get_link_options('Departments', txt);
                                        }
                                    }
                                ],
                                primary_action_label: __("Assign"),
                                primary_action(values) {
                                    if(values.departments && values.departments.length > 0) {
                                        frappe.call({
                                            method: "dynamic.true_lease.api.assign_to_departments",
                                            args: {
                                                docname: frm.doc.name,
                                                departments: values.departments
                                            },
                                            callback: function(r) {
                                                if (r.message) {
                                                    frm.refresh();
                                                }
                                            }
                                        });
                                    }
                                    d.hide();
                                }
                            });
                            d.show();
                        }
                    );
                  }
                }
            }
        });
    }


});