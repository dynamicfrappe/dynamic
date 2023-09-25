


frappe.ui.form.on("Payment Terms Template", {
    refresh:function(frm){
        frm.events.add_child_btn(frm)
    },
    add_child_btn:function(frm){
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Real State")) {
                    frm.fields_dict["terms"].grid.add_custom_button(
                        __("Upload File"),
                        function() {
                          let d = new frappe.ui.Dialog({
                            title: "Enter details",
                            fields: [
                              {
                                label: "Excel File",
                                fieldname: "first_name",
                                fieldtype: "Attach",
                              },
                            ],
                            primary_action_label: "Submit",
                            primary_action(values) {
                              console.log(values);
                              var f = values.first_name;
                              frappe.call({
                                method: "dynamic.real_state.rs_api.add_template_terms",
                                args: {
                                  file: values.first_name,
                                },
                                callback: function(r) {
                                  if (r.message) {
                                    frm.clear_table("terms");
                                    frm.refresh_fields("terms");
                                    // console.log(r.message)
                                    r.message.forEach((element) => {
                                      var row = frm.add_child("terms");
                                      row.payment_term = element.payment_term;
                                      row.description = element.description;
                                      row.invoice_portion = element.invoice_portion;
                                      row.due_date_base_on = element.due_date_base_on;
                                      row.credit_months = element.credit_months;
                                    });
                                    frm.refresh_fields("terms");
                                  }
                                },
                              });
                              d.hide();
                            },
                          });
                  
                          d.show();
                        }
                      ).addClass("btn-primary");;
                }
            }
        }
    })
        
    },

})


frappe.ui.form.on("Payment Terms Template Detail", {
  terms_add(frm, cdt, cdn) { 
    let new_row = locals[cdt][cdn]
    if (new_row.idx >1){
      let prev_row = cur_frm.doc.terms[new_row.idx-2]
      new_row.invoice_portion = prev_row.invoice_portion
      cur_frm.refresh_fields('terms')
      // console.log(prev_row)
    }
}
})
