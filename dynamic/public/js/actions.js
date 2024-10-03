

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
                        var d1 = new frappe.ui.Dialog({
                            title: __("Assign To Departments"),
                            fields: [
                                    {
                                        label: __("Departments"),
                                        fieldname: "departments",
                                        fieldtype: "MultiSelectList",
                                        get_data: function(txt) {
                                            return frappe.db.get_link_options('Departments', txt);
                                        }
                                    },
                            ],
                            primary_action_label: __("Select"),
                            primary_action(values) {
                                if(values.departments && values.departments.length > 0) {
                                    frappe.call({
                                        method: "dynamic.true_lease.api.get_users_by_departments",
                                        args: {
                                            departments: values.departments
                                        },
                                        callback: function(r) {
                                            if (r.message && r.message.users) {
                                                var d2 = new frappe.ui.Dialog({
                                                title: __("Select Users to Assign"),
                                                fields: [
                                                    {
                                                        fieldname: "users_table",
                                                        fieldtype: "Table",
                                                        label: "Users",
                                                        cannot_add_rows: true,
                                                        in_place_edit: false,
                                                        data: r.message.users.map(user => {
                                                            return {
                                                                "user_name": user.full_name,
                                                                "user_email": user.email,
                                                                "selected": 1
                                                            };
                                                        }),
                                                        fields: [
                                                            {
                                                                fieldtype: "Data",
                                                                fieldname: "user_name",
                                                                label: "User Name",
                                                                read_only: 1,
                                                                in_list_view: 1
                                                            },
                                                            {
                                                                fieldtype: "Data",
                                                                fieldname: "user_email",
                                                                label: "Email",
                                                                read_only: 1,
                                                                in_list_view: 1
                                                            },
                                                            {
                                                                fieldtype: "Check",
                                                                fieldname: "selected",
                                                                label: "Select",
                                                                in_list_view: 1
                                                            }
                                                        ]
                                                    }
                                                ],
                                                primary_action_label: __("Assign Selected"),
                                                primary_action (selectedValues) {
                                                    frappe.call({
                                                        method: "dynamic.true_lease.api.assign_users",
                                                        args: {
                                                            docname: frm.doc.name,
                                                            selected_users: selectedValues.users_table
                                                        },
                                                        callback: function (r) {
                                                            if (r.message && r.message.status === "success") {
                                                                frappe.msgprint(__("Assigned to selected users."));
                                                                frm.reload_doc();
                                                            } else {
                                                                frappe.msgprint(r.message.message || __("Assignment failed."));
                                                            }
                                                        }
                                                    });
                                                    d2.hide();
                                                }
                                                });
                                                d2.show();
                                            }
                                            else{
                                                frappe.msgprint(r.message.message);
                                            }
                                        }
                                    });
                                    }
                                    else {
                                        frappe.msgprint(r.message)
                                    }
                                    d1.hide();
                            }
                        });
                        d1.show();

                    });
                            
                }
            }
        } 
        });      
    }
});