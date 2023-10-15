


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
    party:function(frm,cdt,cdn){
      let row = locals[cdt][cdn]
      let doctype_name=''
      let field_name=''
      if (row.party_type == 'Customer'){
        doctype_name = 'Customer'
        field_name = 'customer_name'
      }
      else if (row.party_type == 'Supplier'){
        doctype_name = 'Supplier'
        field_name = 'supplier_name'
      }
      else if (row.party_type == 'Employee'){
        doctype_name = 'Employee'
        field_name = 'employee_name'
      }
      if(doctype_name && field_name){
        frappe.call({
          'method':"frappe.client.get_value",
          'args': {
            'doctype': doctype_name,
            'filters': {
              'name': row.party
            },
             'fieldname':field_name,
          },
          'callback': function(res){

            row.party_name =  res.message[field_name]
            frm.refresh_fields('accounts')
          }
        })
      }
    },
    
})



// frappe.form.link_formatters['Customer'] = function(value, doc) {
//   frappe.call({
//     'method':"frappe.client.get_value",
//     'args': {
//       'doctype': 'Customer',
//       'filters': {
//         'name': value
//       },
//        'fieldname':'customer_name'
//     },
//     'callback': function(res){
//         console.log( res.message.customer_name)

//     }
//   })
	
// }



