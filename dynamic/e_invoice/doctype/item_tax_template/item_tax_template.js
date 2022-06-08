
frappe.ui.form.on("Item Tax Template", {
    setup(frm){
        frm.set_query("tax_type_invoice","taxes",function(doc){
            return {
                filters:{
                 taxtypereference:''   
                }
            }
        })
        frm.set_query("tax_sub_type","taxes",function(doc, cdt, cdn){
            var row = locals [cdt][cdn]
            return {
                filters:{
                 taxtypereference:row.tax_type_invoice
                }
            }
        })
    }
});
