


frappe.ui.form.on('Mode of Payment', {  
	refresh: function(frm) {
        frappe.call({
            method: "dynamic.api.get_active_domains",
            callback: function (r) {
              if (r.message && r.message.length) {
                if (r.message.includes("Payment Deduction")) {

                    frm.set_query("recived_account", function () {
                        return {
                            filters: [
                            ["is_group", "=", 0]
                            ],
                    };})
                    frm.set_query("cost_center", function () {
                        return {
                            filters: [
                            ["is_group", "=", 0]
                            ],
                    };})
                }  
                }
            }
        })

        if(frm.doc.docstatus == 0 && frm.doc.__islocal != 1) {
        frm.add_custom_button(
            __("Show Ledger"),
            function () {
                frappe.set_route('query-report','Mode Of Payment Report',{"mode_of_payment":frm.doc.name,"make_hidden":1})

            },
            __("Show")
          );
        }
	}
    
});