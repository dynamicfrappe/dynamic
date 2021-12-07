// Copyright (c) 2021, Dynamic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tender', {
	// refresh: function(frm) {

	// }
    comparison:(frm)=>{
        let comparison_name = frm.doc.comparison
        if(comparison_name != null){
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Comparison",
                    name: comparison_name,
                },
                callback: function (r) {
                    if (r.message) {
                       let obj =r.message
                        frm.set_value("insurance_rate",obj.insurance_value_rate)
                        frm.set_value("insurance_amount",obj.insurance_value)
                        frm.refresh_field("insurance_rate")
                    }
                },
            });
        }
    },
    insurance_rate:(frm)=>{
        let ins_rate     = parseFloat(frm.doc.insurance_rate)
        let total_amount = parseFloat(frm.doc.total_amount)
        console.log("ins rate",ins_rate)
        console.log("total amount",total_amount)
        let amount = (ins_rate / 100) * total_amount
        frm.set_value("insurance_amount",amount)
        frm.refresh_field("insurance_amount")
    }
});
