


frappe.ui.form.on("Journal Entry", {
    refresh:function(frm){
            frm.events.get_currency_accounts(frm)
    },
    get_currency_accounts:function(frm){
        if(frm.doc.main_currency && frm.doc.account_currency){
            frm.fields_dict["accounts"].grid.get_field("account").get_query = function(doc) {
                return {
                    filters: {
                    'account_currency': doc.account_currency,
                    'company': doc.company,
                    'is_group': 0,
                    }
                }
            
            }
        }
        frm.refresh_fields("accounts")
        
    },
    main_currency:function(frm){
        frm.events.get_currency_accounts(frm)

    },
    account_currency:function(frm){
        frm.events.get_currency_accounts(frm)
    }
})

