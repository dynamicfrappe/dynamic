frappe.ui.form.on("Landed Cost Voucher", {

    domian_valid: function (frm) {
       var tera = false
      frappe.call({
            method :"dynamic.dynamic.validation.get_active_domain" ,
            async: false,
            callback:function (r){
                if (r.message) {
                    tera = true
                }else {
                    tera = false
                }
            }
        })
     return tera

    } ,
    set_up_jebco_query(frm){
        
        frm.set_query("doc_type", "cost_child_table", () => {
            return {
                query :"dynamic.dynamic.validation.get_query_type"
            };
        })
    },
    setup_child_querys(frm){
        frm.fields_dict.cost_child_table.grid.get_field('invoice').get_query =
        function(doc,cdt,cdn) {
			var d = locals[cdt][cdn]
            if (d.doc_type == "Purchase Invoice") {
                return {
                    query : "dynamic.dynamic.validation.get_purchase_items"
                }

            }
            if (d.doc_type== "Payment Entry") {
                var filters = [
                [d.doc_type, 'docstatus', '=', '1'],
                [d.doc_type, 'company', '=', me.frm.doc.company],
            ]
                filters.push(["Payment Entry", "payment_type", "=", "Pay"])
                filters.push(["Payment Entry", "unallocated_amount", ">", "0"])
            }
            return {
                filters: filters
            }
        }
    },
    refresh: function(frm) {  
        // Check If Jebco in Active Domains 
        // This Function will Do Dothing 
        var check_domain = frm.events.domian_valid()
        if (check_domain){
            frm.events.set_up_jebco_query(frm)
            frm.events.setup_child_querys(frm)
        }
    } ,
    add_row_to_charges(frm , doc_type , doc_){
        console.log("DocType" , doc_type)
        console.log("document" ,doc_)
    },
    set_applicabel_charges:function(frm){
        frm.clear_table("taxes")
        frm.refresh_field("taxes")
        var i = 0 
        for (i = 0 ; i < frm.doc.cost_child_table.length ; i ++ ){
            console.log(frm.doc.cost_child_table[i].invoice)
            frm.events.add_row_to_charges(frm,frm.doc.cost_child_table[i].doc_type , frm.doc.cost_child_table[i].invoice )
        }
    }



})


frappe.ui.form.on('Landed Cost Voucher Child', {
    doc_type:function(frm ,cdt,cdn){
        frm.events.setup_child_querys(frm)
    },
    invoice:function(frm , cdt,cdn){
       var  local = locals[cdt][cdn]
       var doc_ument =  local.invoice
       var doctype = local.doc_type
       frappe.call({
           method:"dynamic.terra.landed_cost.get_doctype_info",
           async: false,
           args:{
            doc_type :doctype ,
            document : doc_ument
           },
           callback:function (r){
              if (r.message){
                local.total =  r.message.total
                local.allocated_amount = r.message.allocated
                local.unallocated_amount = 0
                frm.refresh_field("cost_child_table")
                frm.events.set_applicabel_charges(frm)
              }
           }
       })
    }
    


})