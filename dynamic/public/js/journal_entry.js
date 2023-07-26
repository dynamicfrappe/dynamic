


frappe.ui.form.on("Journal Entry Account", {
    account:function(frm,cdt,cdn) {
      console.log("00000000000000000000000000000000000000000")
      var row = locals[cdt][cdn]
      row.account_currency_exchange =1
      frm.set_df_property("account_currency_exchange" , "hidden" , 1) 
      var account = row.account
      var currency = row.account_currency
      console.log("before condition")
      if (currency != frappe.get_doc(":Company", frm.doc.company).default_currency ) {
        console.log("from condition")
        frappe.call({
          "method" :"dynamic.dynamic.utils.currency_valuation_rate" ,
           async: false,
          "args" :{
            "account" : account
          },callback :function(r){
           if (r.message) {
            console.log("message",r.message)
            row.account_currency_exchange = r.message
            frm.refresh_field("accounts")
           }
           
          }
        })
        
      }
  
    },
    
})



