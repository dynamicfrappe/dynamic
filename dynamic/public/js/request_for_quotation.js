frappe.ui.form.on("Request for Quotation", {
    get_stock_uom:function(frm){
        if (frm.doc.items) {
            frm.doc.items.forEach(element => {
                if(element.item_code){
                    frappe.call({
                        method:"frappe.client.get_value",
                        args:{
                            doctype:"Item",
                            fieldname:"stock_uom",
                            "filters": {
                                'name': element.item_code,
                              
                              },
                        },
                        callback:function(r){
                            element.stock_uom = r.message.stock_uom
                        }
                    })
                }
                frm.refresh()
            });
        }
    }
})




frappe.ui.form.on("Request for Quotation Supplier", {
	suppliers_add(frm, cdt, cdn) {
        let supp_row  = locals[cdt][cdn]
        if (supp_row.supplier){
            frm.events.get_stock_uom(frm)
        }
	},

    supplier:function(frm,cdt,cdn){
        let supp_row  = locals[cdt][cdn]
        if (supp_row.supplier){
            frm.events.get_stock_uom(frm)
        }
    }
});