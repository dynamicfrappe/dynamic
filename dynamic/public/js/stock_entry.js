
frappe.ui.form.on("Stock Entry", {
    // setup :function(frm){

    //   frappe.call({
    //       "method" : "dynamic.contracting.doctype.stock_functions.fetch_contracting_data" ,
    //       callback :function(r){
    //         console.log(r)
    //         if (r.message){

    //         }
    //       }
    //   })
       
    // },
    comparison : function (frm) {
        if(frm.doc.against_comparison){

          frappe.call({
            "method" : "dynamic.contracting.doctype.stock_functions.stock_entry_setup" ,
            args:{
              "comparison" : frm.doc.comparison
            },
            callback :function(r){
              if (r.message){

                frm.set_query("comparison_item",function () {
                  return {
                    filters: [
                      ["item_code", "in", r.message],
                     
                    ],
                  };
                });
                frm.refresh_field("comparison_item")
                frm.set_query("comparison_item","items",function () {
                  return {
                    filters: [
                      ["item_code", "in", r.message],
                     
                    ],
                  };
                });
                frm.refresh_field("items")

              }
            } 
         
          })
       
        
        
      
      }
    }


})